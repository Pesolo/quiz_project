from flask import Blueprint, request, jsonify, session  
from app.models import QuizAttempt, Certificate
from app.utils import token_required,  fetch_trivia_questions, calculate_points
import uuid
from app import db

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/quiz')



@quiz_bp.route('/quiz/start', methods=['POST'])
@token_required
def start_quiz(current_user):
    data = request.get_json()
    questions = fetch_trivia_questions(
        data['category'], 
        data['difficulty']
    )
    if not questions:
        return jsonify({'error': 'Failed to fetch questions'}), 500
    
    session['quiz_category'] = data['category']
    

    return jsonify({
        'quiz_id': str(uuid.uuid4()),
        'questions': questions
    })

@quiz_bp.route('/quiz/submit', methods=['POST'])
@token_required
def submit_quiz(current_user):
    data = request.get_json()
    score = int(data['scores'])
    points = calculate_points(score)
    
    attempt = QuizAttempt(
        user_id=current_user.id,
        category=session.get('quiz_category'),
        score=score
    )
    db.session.add(attempt)
    
    current_user.total_points += points
    if current_user.current_level < 5:
        if current_user.total_points >= current_user.current_level * 1000:
            current_user.current_level += 1
            certificate = Certificate(
            user_id=current_user.id,
            level=current_user.current_level
            )
            db.session.add(certificate)

        
    
    db.session.commit()
    
    return jsonify({
        'score': score,
        'points_earned': points,
        'new_level': current_user.current_level,
        'total_points': current_user.total_points
    })