from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Skill
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    skills = Skill.query.order_by(Skill.category, Skill.name).all()
    category_order = request.args.getlist('category')
    if category_order:
        ordered_skills = []
        for cat in category_order:
            ordered_skills.extend([s for s in skills if s.category == cat])
        skills = ordered_skills + [s for s in skills if s.category not in category_order]
    return render_template('index.html', skills=skills, category_order=category_order)

@main.route('/add', methods=['POST'])
def add_skill():
    name = request.form.get('name')
    selected_category = request.form.get('category')
    new_category = request.form.get('new_category')
    category = new_category if new_category else selected_category
    hours = float(request.form.get('hours', 0))

    if name and category:
        new_skill = Skill(name=name, category=category, hours=hours)
        db.session.add(new_skill)
        db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/add-skill')
def add_skill_page():
    categories = sorted(set(skill.category for skill in Skill.query.with_entities(Skill.category).distinct()))
    return render_template('add-skill.html', categories=categories)

@main.route('/skill/<int:skill_id>', methods=['GET', 'POST'])
def skill_detail(skill_id):
    skill = Skill.query.get_or_404(skill_id)

    if request.method == 'POST':
        if 'delete' in request.form:
            db.session.delete(skill)
            db.session.commit()
            return redirect(url_for('main.index'))

        skill.name = request.form.get('name')
        skill.category = request.form.get('category')
        skill.hours = float(request.form.get('hours', 0))
        db.session.commit()
        return redirect(url_for('main.skill_detail', skill_id=skill.id))

    return render_template('skill_detail.html', skill=skill)


@main.route('/add-skill-pack', methods=['POST'])
def add_skill_pack():
    pack = request.form.get('pack')
    skill_sets = {
        'Fitness Freak': [
            ('Weightlifting', 'Fitness'),
            ('Cardio', 'Fitness'),
            ('Yoga', 'Fitness'),
        ],
        'Creative Coder': [
            ('Python', 'Programming'),
            ('Web Dev', 'Programming'),
            ('Game Dev', 'Programming'),
        ],
        'Cyberpunk Toolkit': [
            ('Ethical Hacking', 'Cybersecurity'),
            ('Networking', 'Cybersecurity'),
            ('Linux', 'Cybersecurity'),
        ]
    }

    for name, category in skill_sets.get(pack, []):
        exists = Skill.query.filter_by(name=name, category=category).first()
        if not exists:
            db.session.add(Skill(name=name, category=category))
    db.session.commit()

    flash(f"'{pack}' skill pack added successfully!", 'success')
    return redirect(url_for('main.add_skill_page'))


@main.route('/manage-skills')
def manage_skills():
    skills = Skill.query.order_by(Skill.category, Skill.name).all()
    all_categories = list(set(s.category for s in skills))
    from sqlalchemy import text
    result = db.session.execute(text("SELECT name FROM category_order ORDER BY position ASC"))
    saved_order = [row[0] for row in result]
    categories = sorted(all_categories, key=lambda c: saved_order.index(c) if c in saved_order else len(saved_order))
    return render_template('manage-skills.html', skills=skills, categories=categories)


@main.route('/delete-skill/<int:skill_id>', methods=['POST'])
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash(f"Deleted skill: {skill.name}", 'success')
    return redirect(url_for('main.manage_skills'))


@main.route('/reorder-categories', methods=['POST'])
def reorder_categories():
    from flask import request, jsonify
    request_data = request.get_json()
    category_order = request_data.get("order", [])
    from app.models import db
    db.engine.execute("DELETE FROM category_order")
    for index, name in enumerate(category_order):
        db.engine.execute("INSERT INTO category_order (name, position) VALUES (?, ?)", (name, index))
    return jsonify(success=True)
