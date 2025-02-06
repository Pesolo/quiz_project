from flask import Blueprint, request, jsonify, current_app

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user =data["username"].lower()
        
        if user != "group7" or data["password"] != "password":
            return jsonify({
                'status': 'error',
                'message': 'Invalid credentials'
            }), 401
        
        
        return jsonify({
            'status': 'success',
            'message': 'Welcome Admin'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    

@admin_bp.route('/update', methods=['POST'])
def update_question():
    data = request.get_json()

    if not data:
        return jsonify({
            "status":"unsuccessful",
            "message": "No data"
        }), 400
    
    return jsonify({
        "status":"succesful",
        "message": "Questions updated"
    }), 200