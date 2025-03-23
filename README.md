# Skill Tree App

A gamified life skill tracker inspired by the 10,000-hour rule. Track your real-life skill development, earn levels, and visualize your journey across categories like Tech, Fitness, and Art.

---

## 🚀 Features

- Track time spent on individual skills
- Organize skills by category
- Level-up system based on hours invested
- Add/edit/delete skills
- Drag-and-drop category reordering
- Skill packs for quick onboarding
- Clean, responsive UI for mobile and desktop

---

## 🧠 Concept

Each skill is part of a customizable skill tree. You grow by logging hours:

- **10,000 hours = mastery**
- Skills level up every 10 hours (default)
- Custom level names per skill
- Visualize hours and progress with progress bars

---

## 📁 Project Structure

```bash
Skill-Tree/
├── app/
│   ├── templates/       # HTML files
│   ├── static/          # CSS/JS/assets
│   ├── models.py        # SQLAlchemy models
│   ├── routes.py        # Flask routes (with Blueprint)
│   └── __init__.py      # Flask app factory
├── instance/            # Database and config (if needed)
├── run.py               # Entry point
└── requirements.txt     # Dependencies
```

---

## 🛠️ Tech Stack

- **Frontend:** HTML + CSS + JS (with optional enhancements)
- **Backend:** Python + Flask
- **Database:** SQLite (via SQLAlchemy)
- **Blueprints:** Modular Flask routing
- **ORM:** SQLAlchemy

---

## 🧪 Running the App

```bash
git clone https://github.com/cyb3rm4zy/Skill-Tree.git
cd Skill-Tree
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python run.py
```

App should be running at [http://localhost:5000](http://localhost:5000)

---

## 🔧 Database Setup

If you're not using Flask-Migrate:
```bash
python
>>> from app import db
>>> db.create_all()
```

---

## 📦 Skill Packs

Users can instantly populate their tree with themed packs:
- **Fitness Freak**
- **Creative Coder**
- **Cyberpunk Toolkit**

---

## 📲 Coming Soon

- XP system + Achievements
- PWA (Installable mobile app)
- Graphs and analytics
- Android release via Google Play

---

## 🧠 Credits

Project developed by [cyb3rm4zy](https://github.com/cyb3rm4zy) — a self-improvement companion app to help you master life, one skill at a time.

