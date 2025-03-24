from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    # Create Flask app with explicit instance path
    instance_path = os.path.join(os.getcwd(), 'instance')
    app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)
    app.config.from_object(config_class)
    
    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    print(f"Instance path: {app.instance_path}")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Import models here so they are registered properly
    from .models import User, Category, Skill, JournalEntry

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import auth, skills, main
    from app.routes.manage import bp as manage_bp
    app.register_blueprint(auth.bp)
    app.register_blueprint(skills.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(manage_bp)

    return app
