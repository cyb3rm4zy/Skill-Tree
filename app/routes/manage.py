from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.category import Category
from app.models.skill import Skill
from app import db
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('manage', __name__)

@bp.route('/manage')
@login_required
def manage():
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.position).all()
    return render_template('manage.html', categories=categories)

@bp.route('/api/categories/reorder', methods=['POST'])
@login_required
def reorder_categories():
    try:
        new_order = request.json.get('order', [])
        if not new_order:
            return jsonify({'success': False, 'error': 'No order provided'})
            
        for position, category_id in enumerate(new_order):
            category = Category.query.get_or_404(category_id)
            if category.user_id != current_user.id:
                return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            category.position = position
            
        db.session.commit()
        return jsonify({'success': True})
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({'success': False, 'error': 'Database error'})

@bp.route('/api/category/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        if category.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            
        # Check if this is the last category
        total_categories = Category.query.filter_by(user_id=current_user.id).count()
        if total_categories <= 1:
            return jsonify({'success': False, 'error': 'Cannot delete the last category'})
            
        # Delete all skills in the category first
        Skill.query.filter_by(category_id=category_id).delete()
            
        # Delete all subcategories first
        Category.query.filter_by(parent_id=category_id).delete()
            
        # Delete the category itself
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({'success': False, 'error': 'Database error'})

@bp.route('/api/skill/<int:skill_id>', methods=['DELETE'])
@login_required
def delete_skill(skill_id):
    try:
        skill = Skill.query.get_or_404(skill_id)
        if skill.category.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            
        # Check if this is the last skill in the category
        total_skills = Skill.query.filter_by(category_id=skill.category_id).count()
        category = skill.category
        
        # Delete the skill
        db.session.delete(skill)
        
        # If this was the last skill, delete the category too
        if total_skills <= 1:
            db.session.delete(category)
            
        db.session.commit()
        
        return jsonify({'success': True})
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({'success': False, 'error': 'Database error'}) 