from flask import Blueprint, jsonify
from app.models import User, QuizAttempt
from app.utils import token_required

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')

@profile_bp.route('/', methods=['GET'])
@token_required
def get_profile(current_user):
    """
    Get user profile information including username, scores, level and quiz history.
    Requires authentication token.
    Returns:
        JSON object containing user profile data
    """
    try:
        # Get user's quiz attempts with relevant information
        quiz_history = []
        for quiz in current_user.quizzes:
            quiz_history.append({
                'quiz_id': quiz.id,
                'score': int(quiz.score),
                'total_questions': 10,
                'percentage': round((quiz.score / quiz.total_questions) * 100, 2) if quiz.total_questions > 0 else 0,
                'completed_at': quiz.date_attempted.strftime("%Y-%m-%d %H:%M:%S"),
                'category': quiz.category
            })

        # Prepare response data
        profile_data = {
            'username': current_user.username,
            'total_points': current_user.total_points,
            'current_level': current_user.current_level,
            'quiz_history': quiz_history,
            'total_quizzes_taken': len(quiz_history),
            'average_score': round(sum(quiz['percentage'] for quiz in quiz_history) / len(quiz_history), 2) if quiz_history else 0
        }

        return jsonify({
            'status': 'success',
            'data': profile_data
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch profile data',
            'error': str(e)
        }), 500