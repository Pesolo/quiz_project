from flask import Blueprint, request, jsonify, send_file
from app.models import Certificate
from app.utils import token_required, generate_certificate_image

cert_bp = Blueprint('certificate', __name__, url_prefix='/api/certificates')

@cert_bp.route('/certificates/generate/<int:cert_id>', methods=['GET'])
@token_required
def generate_certificate(cert_id):
    certificate = Certificate.query.get_or_404(cert_id)
    if certificate.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    cert_image = generate_certificate_image(current_user, certificate)
    return send_file(
        cert_image,
        mimetype='image/png',
        as_attachment=True,
        download_name=f'certificate_{cert_id}.png'
    )