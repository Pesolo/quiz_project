from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app import db
from app.utils import token_required
import jwt
from datetime import datetime, timedelta, timezone

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'status': 'error',
                'message': 'Username already exists'
            }), 400
        
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        # Generate token for immediate login after registration
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }, current_app.config['SECRET_KEY'])
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'token': token,
            'user_id': user.id,
            'username': user.username,
            'redirect': '/profile'  # Add redirect URL
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'status': 'error',
                'message': 'Invalid credentials'
            }), 401
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, current_app.config['SECRET_KEY'])
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'token': token,
            'user_id': user.id,
            'username': user.username,
            'redirect': '/profile'  # Add redirect URL
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# # Optional: Add route to verify token and get user info
# @auth_bp.route('/verify', methods=['GET'])
# @token_required
# def verify_token(current_user):
#     return jsonify({
#         'status': 'success',
#         'user_id': current_user.id,
#         'username': current_user.username
#     })