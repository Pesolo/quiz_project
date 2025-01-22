from app import db
from datetime import datetime, timezone

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    date_attempted = db.Column(db.DateTime, default=datetime.now(timezone.utc))