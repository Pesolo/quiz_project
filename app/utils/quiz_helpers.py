import requests
from typing import List, Dict, Any

def calculate_score(quiz_data: Dict[str, Any]) -> int:
    """Calculate the score based on correct answers"""
    return sum(1 for answer in quiz_data['answers'] if answer['correct'])

def calculate_points(difficulty: str, correct_answers: int) -> int:
    """Calculate points based on difficulty and correct answers"""
    difficulty_multiplier = {
        'easy': 1,
        'medium': 2,
        'hard': 3
    }
    return correct_answers * 10 * difficulty_multiplier[difficulty]

def fetch_trivia_questions(category: str, difficulty: str, amount: int = 10) -> List[Dict[str, Any]]:
    """Fetch and format trivia questions"""
    category_mapping = {
        'water': 17,    # Science & Nature
        'energy': 17,
        'waste': 17,
        'biodiversity': 27  # Animals
    }
    
    api_category = category_mapping.get(category, 17)
    url = f'https://opentdb.com/api.php?amount={amount}&category={api_category}&difficulty={difficulty}&type=multiple'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            questions = data['results']
            
            # Format questions for conservation focus
            for q in questions:
                if category == 'water':
                    q['question'] = f"Regarding water conservation: {q['question']}"
                elif category == 'energy':
                    q['question'] = f"In the context of energy efficiency: {q['question']}"
            
            return questions
    except requests.exceptions.RequestException:
        return None
    
    return None