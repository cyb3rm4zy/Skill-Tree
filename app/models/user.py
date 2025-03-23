from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Skill tree related fields
    categories = db.relationship('Category', backref='user', lazy=True)
    total_hours = db.Column(db.Float, default=0.0)
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def add_xp(self, amount):
        self.xp += amount
        # Level up logic (can be adjusted)
        while self.xp >= self.level * 100:
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.xp -= (self.level - 1) * 100 