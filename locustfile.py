"""
Locust load testing script for the Riddle Game.
Since the game is a desktop GUI application, this script tests the core game logic
and simulates user interactions with the riddle system.
"""
from locust import User, task, between
import time
import random
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from riddles_data import riddles
except ImportError:
    # Fallback riddles if import fails
    riddles = [
        {"question": "Test question?", "answer": "test", "hint": "Test hint."}
    ]

class RiddleGameUser(User):
    """
    Simulates a user playing the riddle game.
    Tests the core game logic under load.
    """
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Initialize user session."""
        self.username = f"LoadTestUser_{random.randint(1000, 9999)}"
        self.age = random.randint(21, 65)
        self.score = 0
        self.current_riddle_index = 0
        self.session_start_time = time.time()
        
    @task(3)
    def validate_user_data(self):
        """Test user data validation logic."""
        start_time = time.time()
        
        try:
            # Simulate username validation
            name = self.username.strip()
            if not name:
                self.environment.events.request.fire(
                    request_type="VALIDATION",
                    name="username_empty",
                    response_time=(time.time() - start_time) * 1000,
                    response_length=0,
                    exception=Exception("Username cannot be empty!")
                )
                return
            
            # Simulate age validation  
            if self.age < 21:
                self.environment.events.request.fire(
                    request_type="VALIDATION", 
                    name="age_too_young",
                    response_time=(time.time() - start_time) * 1000,
                    response_length=0,
                    exception=Exception("Too Young to Play!")
                )
                return
                
            # Success case
            self.environment.events.request.fire(
                request_type="VALIDATION",
                name="user_data_valid", 
                response_time=(time.time() - start_time) * 1000,
                response_length=len(self.username)
            )
            
        except Exception as e:
            self.environment.events.request.fire(
                request_type="VALIDATION",
                name="validation_error",
                response_time=(time.time() - start_time) * 1000, 
                response_length=0,
                exception=e
            )
    
    @task(5)
    def load_riddle(self):
        """Test riddle loading performance."""
        start_time = time.time()
        
        try:
            if self.current_riddle_index >= len(riddles):
                # Game over - reset for continued testing
                self.current_riddle_index = 0
                self.score = 0
                
            riddle = riddles[self.current_riddle_index]
            riddle_data = {
                "question": riddle["question"],
                "answer": riddle["answer"], 
                "hint": riddle["hint"]
            }
            
            # Simulate processing time for UI rendering
            time.sleep(0.01)  # 10ms for UI update simulation
            
            self.environment.events.request.fire(
                request_type="GAME",
                name="load_riddle",
                response_time=(time.time() - start_time) * 1000,
                response_length=len(riddle_data["question"])
            )
            
        except Exception as e:
            self.environment.events.request.fire(
                request_type="GAME", 
                name="load_riddle_error",
                response_time=(time.time() - start_time) * 1000,
                response_length=0,
                exception=e
            )
    
    @task(7)
    def check_answer(self):
        """Test answer checking logic."""
        start_time = time.time()
        
        try:
            if self.current_riddle_index >= len(riddles):
                return
                
            riddle = riddles[self.current_riddle_index]
            correct_answer = riddle["answer"]
            
            # Simulate different user answer scenarios
            answer_scenarios = [
                correct_answer,  # Correct answer
                correct_answer.upper(),  # Correct but uppercase
                f" {correct_answer} ",  # Correct with whitespace
                "wrong_answer",  # Wrong answer
                "",  # Empty answer
                correct_answer + "typo"  # Almost correct
            ]
            
            user_answer = random.choice(answer_scenarios)
            processed_answer = user_answer.strip().lower()
            
            if processed_answer == correct_answer:
                # Correct answer
                self.score += 1
                self.current_riddle_index += 1
                result = "correct"
            else:
                # Incorrect answer - show hint
                result = "incorrect"
            
            self.environment.events.request.fire(
                request_type="GAME",
                name=f"check_answer_{result}",
                response_time=(time.time() - start_time) * 1000, 
                response_length=len(user_answer)
            )
            
        except Exception as e:
            self.environment.events.request.fire(
                request_type="GAME",
                name="check_answer_error", 
                response_time=(time.time() - start_time) * 1000,
                response_length=0,
                exception=e
            )
    
    @task(1)
    def calculate_final_score(self):
        """Test final score calculation."""
        start_time = time.time()
        
        try:
            total_riddles = len(riddles)
            percentage = (self.score / total_riddles) * 100 if total_riddles > 0 else 0
            score_message = f"You got {self.score} out of {total_riddles} correct!"
            
            # Simulate score display processing
            time.sleep(0.005)  # 5ms for score calculation
            
            self.environment.events.request.fire(
                request_type="GAME",
                name="calculate_score",
                response_time=(time.time() - start_time) * 1000,
                response_length=len(score_message)
            )
            
        except Exception as e:
            self.environment.events.request.fire(
                request_type="GAME", 
                name="calculate_score_error",
                response_time=(time.time() - start_time) * 1000,
                response_length=0,
                exception=e
            )
    
    @task(1) 
    def stress_test_riddles_access(self):
        """Stress test rapid riddle data access."""
        start_time = time.time()
        
        try:
            # Rapidly access multiple riddles to test data structure performance
            accessed_riddles = []
            for i in range(min(10, len(riddles))):
                riddle_index = random.randint(0, len(riddles) - 1)
                riddle = riddles[riddle_index]
                accessed_riddles.append({
                    "index": riddle_index,
                    "question_length": len(riddle["question"]),
                    "answer_length": len(riddle["answer"]),
                    "hint_length": len(riddle["hint"])
                })
            
            total_data_size = sum(
                r["question_length"] + r["answer_length"] + r["hint_length"] 
                for r in accessed_riddles
            )
            
            self.environment.events.request.fire(
                request_type="STRESS",
                name="rapid_riddle_access",
                response_time=(time.time() - start_time) * 1000,
                response_length=total_data_size
            )
            
        except Exception as e:
            self.environment.events.request.fire(
                request_type="STRESS",
                name="rapid_access_error", 
                response_time=(time.time() - start_time) * 1000,
                response_length=0,
                exception=e
            )

class AdminUser(User):
    """
    Simulates administrative operations on the game.
    """
    wait_time = between(5, 10)
    weight = 1  # Lower weight - fewer admin users
    
    @task
    def validate_riddles_integrity(self):
        """Test riddles data integrity under load."""
        start_time = time.time()
        
        try:
            # Check riddles structure
            assert isinstance(riddles, list), "Riddles should be a list"
            assert len(riddles) > 0, "Riddles should not be empty"
            
            for i, riddle in enumerate(riddles):
                assert isinstance(riddle, dict), f"Riddle {i} should be a dict"
                assert "question" in riddle, f"Riddle {i} missing question"
                assert "answer" in riddle, f"Riddle {i} missing answer" 
                assert "hint" in riddle, f"Riddle {i} missing hint"
            
            self.environment.events.request.fire(
                request_type="ADMIN",
                name="integrity_check_pass",
                response_time=(time.time() - start_time) * 1000,
                response_length=len(riddles)
            )
            
        except Exception as e:
            self.environment.events.request.fire(
                request_type="ADMIN",
                name="integrity_check_fail",
                response_time=(time.time() - start_time) * 1000, 
                response_length=0,
                exception=e
            )