from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Import config after app creation
    from .config import Config
    config_class = config_class or Config
    
    app.config.from_object(config_class)
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    with app.app_context():
        # Import models here to avoid circular imports
        from app.models import user, quiz, certificate

        # Initialize routes
        from app.routes import init_routes
        init_routes(app)


    return app

# Create a default app instance for Gunicorn
app = create_app()

