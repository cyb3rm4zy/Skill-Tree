from . import db

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Float, default=0.0)

    def progress_percent(self):
        return min((self.hours / 10000) * 100, 100)

    def level(self):
        return int(self.hours // 10)

    def level_name(self):
        level = self.level()
        if level < 5:
            return "Novice"
        elif level < 20:
            return "Apprentice"
        elif level < 50:
            return "Expert"
        else:
            return "Master"


class CategoryOrder(db.Model):
    __tablename__ = 'category_order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    position = db.Column(db.Integer, nullable=False)
