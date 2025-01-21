from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here to register them with SQLAlchemy
    from app.models import user, quiz, certificate  # Import models to register with SQLAlchemy

    # Initialize routes (ensure this is a proper blueprint registration)
    from app.routes import init_routes
    init_routes(app)

    return app
