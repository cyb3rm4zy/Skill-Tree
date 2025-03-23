from app import create_app, db
from app.models import User, Category, Skill, JournalEntry
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Category': Category, 
        'Skill': Skill, 
        'JournalEntry': JournalEntry
    }

def init_db():
    # Make sure instance folder exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path, exist_ok=True)
        print(f"Created instance folder at {app.instance_path}")
    
    # Set permissions for the instance folder
    try:
        import stat
        os.chmod(app.instance_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        print(f"Set permissions for instance folder {app.instance_path}")
    except Exception as e:
        print(f"Warning: Could not set permissions on instance folder: {e}")
    
    # Create database
    with app.app_context():
        print(f"Creating database at {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Try to check if tables exist properly - if not, drop all and recreate
        try:
            if User.query.count() == 0:
                print("No users found - database is fresh")
        except Exception as e:
            print(f"Database schema issue detected: {e}")
            print("Dropping all tables and recreating database schema...")
            db.drop_all()
            print("All tables dropped.")
        
        # Create all tables
        db.create_all()
        print("Database tables created successfully")

if __name__ == '__main__':
    try:
        init_db()
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
