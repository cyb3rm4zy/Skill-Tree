from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.skill import Skill, JournalEntry
from app.models.category import Category
from app import db
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('skills', __name__)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_skill():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            category_name = request.form.get('category', '').strip()
            hours = float(request.form.get('hours', 0))
            
            if not name or not category_name:
                flash('Please provide both skill name and category', 'error')
                return redirect(url_for('skills.add_skill'))
            
            # Get or create category
            category = Category.query.filter_by(name=category_name, user_id=current_user.id).first()
            if not category:
                category = Category(name=category_name, user_id=current_user.id)
                db.session.add(category)
                db.session.commit()
            
            # Create skill
            skill = Skill(
                name=name,
                category_id=category.id,
                total_hours=0.0,
                target_hours=10000.0,
                mastery_percentage=0.0,
                level=1,
                level_threshold=10.0
            )
            db.session.add(skill)
            db.session.commit()
            
            if hours > 0:
                skill.add_hours(hours)
                current_user.total_hours += hours
                db.session.commit()
            
            flash('Skill added successfully!', 'success')
            return redirect(url_for('main.index'))
            
        except ValueError:
            flash('Invalid hours value', 'error')
            return redirect(url_for('skills.add_skill'))
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error: {str(e)}")
            flash('An error occurred while adding the skill', 'error')
            return redirect(url_for('skills.add_skill'))
        
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('add-skill.html', categories=[c.name for c in categories])

@bp.route('/add-skill-pack', methods=['POST'])
@login_required
def add_skill_pack():
    try:
        pack_name = request.form.get('pack')
        packs = {
            'Fitness Freak': [
                ('Weightlifting', 'Fitness'),
                ('Cardio', 'Fitness'),
                ('Yoga', 'Fitness')
            ],
            'Creative Coder': [
                ('Python', 'Programming'),
                ('Web Development', 'Programming'),
                ('Game Development', 'Programming')
            ],
            'Cyberpunk Toolkit': [
                ('Ethical Hacking', 'Security'),
                ('Networking', 'Security'),
                ('Linux', 'Operating Systems')
            ]
        }
        
        if pack_name in packs:
            for skill_name, category_name in packs[pack_name]:
                # Get or create category
                category = Category.query.filter_by(name=category_name, user_id=current_user.id).first()
                if not category:
                    category = Category(name=category_name, user_id=current_user.id)
                    db.session.add(category)
                    db.session.commit()
                
                # Create skill
                skill = Skill(name=skill_name, category_id=category.id, total_hours=0.0, target_hours=10000.0)
                db.session.add(skill)
            
            db.session.commit()
            flash(f'{pack_name} skill pack added successfully!', 'success')
        else:
            flash('Invalid skill pack', 'error')
            
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        flash('An error occurred while adding the skill pack', 'error')
    
    return redirect(url_for('main.index'))

@bp.route('/skill/<int:skill_id>/add-hours', methods=['POST'])
@login_required
def add_hours(skill_id):
    try:
        skill = Skill.query.get_or_404(skill_id)
        if skill.category.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            
        hours = float(request.form.get('hours', 0))
        
        if hours > 0:
            skill.add_hours(hours)
            # Update user's total hours directly
            current_user.total_hours += hours
            db.session.commit()
            return jsonify({
                'success': True,
                'total_hours': skill.total_hours,
                'mastery_percentage': skill.mastery_percentage,
                'level': skill.level,
                'level_name': skill.get_level_name()
            })
        
        return jsonify({'success': False, 'error': 'Invalid hours'})
        
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid hours value'})
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({'success': False, 'error': 'Database error'})

@bp.route('/skill/<int:skill_id>/change-category', methods=['POST'])
@login_required
def change_category(skill_id):
    try:
        skill = Skill.query.get_or_404(skill_id)
        if skill.category.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            
        category_name = request.form.get('category', '').strip()
        
        if not category_name:
            return jsonify({'success': False, 'error': 'Category name is required'})
        
        # Handle case where category doesn't change
        if category_name == skill.category.name:
            return jsonify({'success': True})
            
        # Get or create category
        category = Category.query.filter_by(name=category_name, user_id=current_user.id).first()
        if not category:
            category = Category(name=category_name, user_id=current_user.id)
            db.session.add(category)
            
        # Update old category stats
        old_category = skill.category
        
        # Change skill category
        skill.category_id = category.id
        db.session.commit()
        
        # Update stats for both categories
        old_category.update_stats()
        category.update_stats()
        db.session.commit()
        
        return jsonify({'success': True})
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({'success': False, 'error': 'Database error'})

@bp.route('/skill/<int:skill_id>/journal', methods=['POST'])
@login_required
def add_journal_entry(skill_id):
    try:
        skill = Skill.query.get_or_404(skill_id)
        if skill.category.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            
        content = request.form.get('content', '').strip()
        
        if content:
            entry = JournalEntry(content=content, skill_id=skill.id)
            db.session.add(entry)
            db.session.commit()
            return jsonify({
                'success': True,
                'entry': {
                    'id': entry.id,
                    'content': entry.content,
                    'created_at': entry.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        
        return jsonify({'success': False, 'error': 'Invalid content'})
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({'success': False, 'error': 'Database error'}) 