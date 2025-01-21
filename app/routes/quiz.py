from flask import Blueprint, request, jsonify
from app.models import QuizAttempt
from app.utils import token_required, calculate_score, fetch_trivia_questions, calculate_points
import uuid

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/quiz')

@quiz_bp.route('/quiz/start', methods=['POST'])
@token_required
def start_quiz():
    data = request.get_json()
    questions = fetch_trivia_questions(
        data['category'], 
        data['difficulty']
    )
    if not questions:
        return jsonify({'error': 'Failed to fetch questions'}), 500
    
    return jsonify({
        'quiz_id': str(uuid.uuid4()),
        'questions': questions
    })

@quiz_bp.route('/quiz/submit', methods=['POST'])
@token_required
def submit_quiz():
    data = request.get_json()
    score = calculate_score(data['quiz_data'])
    points = calculate_points(data['quiz_data']['difficulty'], score)
    
    attempt = QuizAttempt(
        user_id=current_user.id,
        category=data['quiz_data']['category'],
        score=score,
        difficulty=data['quiz_data']['difficulty']
    )
    db.session.add(attempt)
    
    current_user.total_points += points
    if current_user.total_points >= current_user.current_level * 1000:
        current_user.current_level += 1
        
    
    db.session.commit()
    
    return jsonify({
        'score': score,
        'points_earned': points,
        'new_level': current_user.current_level,
        'total_points': current_user.total_points
    })