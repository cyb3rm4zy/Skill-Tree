from app import db
from datetime import datetime

class Skill(db.Model):
    __tablename__ = 'skill'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Skill progress tracking
    total_hours = db.Column(db.Float, default=0.0)
    mastery_percentage = db.Column(db.Float, default=0.0)
    level = db.Column(db.Integer, default=1)
    
    # Skill specific settings
    target_hours = db.Column(db.Float, default=10000.0)  # Default to 10,000 hour rule
    level_threshold = db.Column(db.Float, default=10.0)  # Hours needed per level
    
    # Journal entries
    journal_entries = db.relationship('JournalEntry', backref='skill', lazy=True)
    
    def add_hours(self, hours):
        """Add hours to the skill and update related stats"""
        self.total_hours += hours
        self.mastery_percentage = (self.total_hours / self.target_hours) * 100
        
        # Update level based on hours
        new_level = int(self.total_hours / self.level_threshold) + 1
        if new_level > self.level:
            self.level = new_level
            
        # Update parent category stats
        self.category.update_stats()
        
    def get_level_name(self):
        """Get the current level name based on mastery percentage"""
        if self.mastery_percentage < 10:
            return "Novice"
        elif self.mastery_percentage < 25:
            return "Apprentice"
        elif self.mastery_percentage < 50:
            return "Intermediate"
        elif self.mastery_percentage < 75:
            return "Advanced"
        elif self.mastery_percentage < 100:
            return "Expert"
        else:
            return "Master"

class JournalEntry(db.Model):
    __tablename__ = 'journal_entry'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False) 