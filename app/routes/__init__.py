from flask import Blueprint
from .auth import auth_bp
from .quiz import quiz_bp
from .certificate import cert_bp
from .profile import profile_bp

# Register all blueprints
def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(cert_bp)
    app.register_blueprint(profile_bp)