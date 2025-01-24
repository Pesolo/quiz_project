import json
import random
import os
from typing import List, Dict, Any

def calculate_score(quiz_data: Dict[str, Any]) -> int:
    """Calculate the score based on correct answers"""
    return sum(1 for answer in quiz_data['answers'] if answer['correct'])

def calculate_points(difficulty: str, correct_answers: int) -> int:
    """Calculate points based on difficulty and correct answers"""
    difficulty_multiplier = {
        'easy': 2,
        'medium': 2,
        'hard': 2
    }
    return correct_answers * 10 * difficulty_multiplier[difficulty]

def fetch_trivia_questions(category: str, difficulty: str, amount: int = 10) -> List[Dict[str, Any]]:
    """Fetch and format trivia questions from local files"""
    category_mapping = {
        'water': 'water.json',
        'food': 'food.json',
        'forest': 'forest.json',
        'mineral': 'mineral.json'  # Example: if biodiversity is handled by 'mineral.json'
    }
    
    # Determine the file corresponding to the category
    file_name = category_mapping.get(category)
    
    if not file_name:
        return None  # Invalid category
    
    # Load questions from the JSON file
    try:
        file_path = os.path.join('questions', file_name)
        with open(file_path, 'r') as f:
            questions = json.load(f)
        
        # Pick a random sample of questions
        selected_questions = random.sample(questions, min(amount, len(questions)))
        
        # Format questions for the category
        for q in selected_questions:
            if category == 'water':
                q['question'] = f"Regarding Water Conservation: {q['question']}"
            elif category == 'forest':
                q['question'] = f"Regarding Forest Conservation: {q['question']}"
            elif category == 'mineral':
                q['question'] = f"Regarding Mineral Conservation: {q['question']}"
            elif category == 'food':
                q['question'] = f"Regarding Food Conservation: {q['question']}"
            
        return selected_questions
    
    except (FileNotFoundError, json.JSONDecodeError):
        return None