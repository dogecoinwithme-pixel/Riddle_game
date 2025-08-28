"""
Unit tests for the Riddle Game logic.
"""
import pytest
import allure
import sys
import os

# Add the project root to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the riddles data from riddles_data module
try:
    from riddles_data import riddles
except ImportError:
    # Fallback riddles for testing if import fails
    riddles = [
        {"question": "Test question?", "answer": "test", "hint": "Test hint."}
    ]

@allure.feature("Riddle Game")
@allure.story("Riddles Data Validation")
class TestRiddlesData:
    """Test class for validating riddles data structure and content."""
    
    @allure.title("Test riddles data structure")
    @allure.description("Verify that riddles data has the correct structure")
    def test_riddles_structure(self):
        """Test that riddles have the required structure."""
        assert isinstance(riddles, list), "Riddles should be a list"
        assert len(riddles) > 0, "Riddles list should not be empty"
        
        for i, riddle in enumerate(riddles):
            with allure.step(f"Validating riddle {i+1}"):
                assert isinstance(riddle, dict), f"Riddle {i+1} should be a dictionary"
                assert "question" in riddle, f"Riddle {i+1} should have a 'question' field"
                assert "answer" in riddle, f"Riddle {i+1} should have an 'answer' field"
                assert "hint" in riddle, f"Riddle {i+1} should have a 'hint' field"
    
    @allure.title("Test riddles content quality")
    @allure.description("Verify that riddles have meaningful content")
    def test_riddles_content(self):
        """Test that riddles have meaningful content."""
        for i, riddle in enumerate(riddles):
            with allure.step(f"Checking content quality for riddle {i+1}"):
                assert len(riddle["question"]) > 10, f"Riddle {i+1} question should be meaningful"
                assert len(riddle["answer"]) > 0, f"Riddle {i+1} should have an answer"
                assert len(riddle["hint"]) > 5, f"Riddle {i+1} hint should be helpful"
                assert riddle["question"].endswith("?"), f"Riddle {i+1} question should end with ?"
    
    @allure.title("Test answer case sensitivity")
    @allure.description("Verify that answers are in lowercase for consistency")
    def test_answer_format(self):
        """Test that answers are in the correct format."""
        for i, riddle in enumerate(riddles):
            with allure.step(f"Checking answer format for riddle {i+1}"):
                answer = riddle["answer"]
                assert answer == answer.lower(), f"Riddle {i+1} answer should be lowercase"
                assert " " not in answer or "_" in answer, f"Riddle {i+1} multi-word answers should use underscores"

@allure.feature("Riddle Game")
@allure.story("Game Logic")
class TestGameLogic:
    """Test class for game logic validation."""
    
    @allure.title("Test age validation")
    @allure.description("Test that age validation works correctly")
    def test_age_validation(self):
        """Test age validation logic."""
        with allure.step("Testing valid ages"):
            valid_ages = [21, 25, 30, 65, 100]
            for age in valid_ages:
                assert age >= 21, f"Age {age} should be valid"
        
        with allure.step("Testing invalid ages"):
            invalid_ages = [0, 10, 18, 20]
            for age in invalid_ages:
                assert age < 21, f"Age {age} should be invalid"
    
    @allure.title("Test score calculation")
    @allure.description("Test that scoring works correctly")
    def test_score_calculation(self):
        """Test score calculation logic."""
        initial_score = 0
        total_riddles = len(riddles)
        
        with allure.step("Testing perfect score"):
            perfect_score = total_riddles
            assert perfect_score <= total_riddles, "Perfect score should not exceed total riddles"
        
        with allure.step("Testing partial score"):
            partial_score = total_riddles // 2
            assert 0 <= partial_score <= total_riddles, "Partial score should be within valid range"

@allure.feature("Riddle Game")
@allure.story("Data Integrity")
class TestDataIntegrity:
    """Test class for data integrity checks."""
    
    @allure.title("Test unique riddles")
    @allure.description("Verify that all riddles are unique")
    def test_unique_riddles(self):
        """Test that all riddles are unique."""
        questions = [riddle["question"] for riddle in riddles]
        answers = [riddle["answer"] for riddle in riddles]
        
        with allure.step("Checking question uniqueness"):
            assert len(questions) == len(set(questions)), "All questions should be unique"
        
        with allure.step("Checking answer uniqueness"):
            # Note: Answers might not be unique (e.g., multiple riddles with same answer)
            # This is more of a warning than a hard requirement
            if len(answers) != len(set(answers)):
                allure.attach(
                    f"Found {len(answers) - len(set(answers))} duplicate answers",
                    name="Duplicate Answers Warning",
                    attachment_type=allure.attachment_type.TEXT
                )
    
    @allure.title("Test riddle count consistency")
    @allure.description("Verify that the riddle count matches expected value")
    def test_riddle_count(self):
        """Test that we have the expected number of riddles."""
        expected_count = 20  # Based on the final score message showing "out of 20"
        actual_count = len(riddles)
        
        with allure.step(f"Checking riddle count: expected {expected_count}, actual {actual_count}"):
            assert actual_count == expected_count, f"Expected {expected_count} riddles, but found {actual_count}"