from flask import Blueprint, request, jsonify, send_file
from app.models import Certificate
from app.utils import token_required, generate_certificate_image

cert_bp = Blueprint('certificate', __name__, url_prefix='/api/certificates')

@cert_bp.route('/certificates/generate', methods=['GET'])
@token_required
def generate_certificate(current_user):
    # Fetch the latest certificate for the current user
    certificate = current_user.get_latest_certificate()
    
    if not certificate:
        return jsonify({'error': 'No certificate found for the user'}), 404
    
    # Generate the certificate image
    cert_image = generate_certificate_image(current_user, certificate)
    
    # Return the image as a downloadable file
    return send_file(
        cert_image,
        mimetype='image/png',
        as_attachment=True,
        download_name=f'certificate_{certificate.id}.png'
    )