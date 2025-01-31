from flask import Blueprint, request, jsonify, send_file
from app.models import Certificate, User
from app.utils import token_required
from datetime import datetime

cert_bp = Blueprint('certificate', __name__, url_prefix='/api/certificates')

@cert_bp.route('/generate', methods=['GET'])
@token_required
def generate_certificate(current_user):
    try:
        # Input validation
        if not hasattr(current_user, 'username') or not current_user.username:
            raise ValueError("Invalid user object: missing username")
            
        # Fetch the latest certificate for the current user
        certificate = current_user.get_latest_certificate()
        
        if not certificate:
            return jsonify({'error': 'No certificate found for the user'}), 404
            
        if not all(hasattr(certificate, attr) for attr in ['id', 'level', 'date_earned']):
            raise ValueError("Invalid certificate object: missing required attributes")
        
        try:
            date_str = certificate.date_earned.strftime('%Y-%m-%d')
        except AttributeError:
            date_str = datetime.now().strftime('%Y-%m-%d')
            print("Warning: Using current date as certificate date was invalid")

        cert_data = {
            "fullname": current_user.fullname,
            "level": certificate.level,
            "date_earned": date_str
        }

        return jsonify({
            'status': 'success',
            'data': cert_data
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to generate certificate',
            'message': str(e)
        }), 500

