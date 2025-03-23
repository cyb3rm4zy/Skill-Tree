import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    # Using a relative path that Flask will resolve relative to the instance folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # PWA settings
    PWA_NAME = 'Life Stats Tracker'
    PWA_DESCRIPTION = 'Track your life skills and progress'
    PWA_THEME_COLOR = '#0A0302'
    PWA_BACKGROUND_COLOR = '#ffffff'
    PWA_DISPLAY = 'standalone'
    PWA_ORIENTATION = 'any'
    PWA_START_URL = '/'
    PWA_ICONS = [
        {
            'src': '/static/images/icon-192x192.png',
            'sizes': '192x192',
            'type': 'image/png'
        },
        {
            'src': '/static/images/icon-512x512.png',
            'sizes': '512x512',
            'type': 'image/png'
        }
    ] 