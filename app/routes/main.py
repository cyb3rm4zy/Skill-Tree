from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.category import Category
from app.models.skill import Skill

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('landing.html')
    
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', categories=categories)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/skill/<int:skill_id>')
@login_required
def skill_detail(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.category.user_id != current_user.id:
        return redirect(url_for('main.index'))
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('skill_detail.html', skill=skill, categories=categories) 