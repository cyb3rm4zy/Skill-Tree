from app import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    # Relationships
    skills = db.relationship('Skill', backref='category', lazy=True)
    subcategories = db.relationship('Category',
                                  backref=db.backref('parent', remote_side=[id]),
                                  lazy=True)
    
    # Category specific stats
    total_hours = db.Column(db.Float, default=0.0)
    mastery_percentage = db.Column(db.Float, default=0.0)
    
    def update_stats(self):
        """Update category stats based on skills and subcategories"""
        self.total_hours = sum(skill.total_hours for skill in self.skills)
        self.total_hours += sum(cat.total_hours for cat in self.subcategories)
        self.mastery_percentage = (self.total_hours / 10000) * 100 