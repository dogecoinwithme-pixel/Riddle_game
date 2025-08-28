"""
Riddles data module - extracted for testing purposes.
This allows testing of riddles data without GUI dependencies.
"""

# Riddles, answers, and hints
riddles = [
    {"question": "What's always hard to keep in your pants when you're excited?", "answer": "phone", "hint": "It's something you check often."},
    {"question": "What grows bigger the more you play with it?", "answer": "ego", "hint": "It's inflated by compliments."},
    {"question": "What's slippery when wet and hard to hold onto?", "answer": "soap", "hint": "It's used in the shower."},
    {"question": "What's long, gets hot, and you grip it tightly?", "answer": "candle", "hint": "It's lit during a romantic evening."},
    {"question": "What's something you blow to make it quick?", "answer": "fuse", "hint": "It's part of an explosive."},
    {"question": "What's firm, juicy, and best when squeezed?", "answer": "peach", "hint": "It's a fruit you eat."},
    {"question": "What's soft, gets wet, and you rub it in circles?", "answer": "towel", "hint": "It's used after a shower."},
    {"question": "What's stiff, stands up, and you adjust it in the morning?", "answer": "collar", "hint": "It's part of a dress shirt."},
    {"question": "What's something you stroke to make it purr?", "answer": "cat", "hint": "It's a pet that loves attention."},
    {"question": "What's round, bouncy, and fun to chase?", "answer": "ball", "hint": "It's used in sports."},
    {"question": "What's sticky, sweet, and drips when warm?", "answer": "honey", "hint": "It's made by bees."},
    {"question": "What's hard, gets pounded, and you do it on a table?", "answer": "nail", "hint": "It's used in carpentry."},
    {"question": "What's something you lick before you stick?", "answer": "stamp", "hint": "It's used for mailing letters."},
    {"question": "What's long, curved, and you peel it before use?", "answer": "banana", "hint": "It's a fruit you eat."},
    {"question": "What's tight, stretchy, and you slip into it?", "answer": "glove", "hint": "It protects your hands."},
    {"question": "What's hot, steamy, and you do it in a bath?", "answer": "tea", "hint": "It's a beverage you steep."},
    {"question": "What's something you pump to make it quick?", "answer": "tire", "hint": "It's part of a car."},
    {"question": "What's smooth, gets wet, and you slide it in?", "answer": "card", "hint": "It's used for payments."},
    {"question": "What's something you whip to make it quick and creamy?", "answer": "cream", "hint": "It's used in desserts."},
    {"question": "What's hard to pull out once it's in deep?", "answer": "cork", "hint": "It's used to seal a bottle."}
]

def validate_start(name, age_text):
    """
    Validate user input for starting the game.
    This function is extracted for testing purposes.
    """
    if not name:
        return False, "Username cannot be empty!"
    
    try:
        age = int(age_text)
        if age < 21:
            return False, "Too Young to Play!"
    except ValueError:
        return False, "Age must be a number!"
    
    return True, "Valid input"

def check_answer(user_answer, correct_answer):
    """
    Check if user answer matches the correct answer.
    This function is extracted for testing purposes.
    """
    processed_answer = user_answer.strip().lower()
    return processed_answer == correct_answer

def calculate_score(score, total_riddles):
    """
    Calculate final score and percentage.
    This function is extracted for testing purposes.
    """
    percentage = (score / total_riddles) * 100 if total_riddles > 0 else 0
    return {
        'score': score,
        'total': total_riddles,
        'percentage': percentage,
        'message': f"You got {score} out of {total_riddles} correct!"
    }