import bcrypt
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    current_level = db.Column(db.Integer, default=1)
    total_points = db.Column(db.Integer, default=0)
    quizzes = db.relationship('QuizAttempt', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)

    def set_password(self, password):
        # Hash the password and store it
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
    def check_password(self, password):
        # Compare the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def get_latest_certificate(self):
        # Fetch the latest certificate for the user
        from app.models import Certificate
        return Certificate.query.filter_by(user_id=self.id).order_by(Certificate.date_earned.desc()).first()
