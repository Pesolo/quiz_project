from app import db
from datetime import datetime, timezone

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    date_earned = db.Column(db.DateTime, default=datetime.now(timezone.utc))