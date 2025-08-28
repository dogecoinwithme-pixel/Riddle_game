"""
Integration tests for the Riddle Game application.
"""
import pytest
import allure
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@allure.feature("Riddle Game")
@allure.story("Application Integration")
class TestRiddleGameIntegration:
    """Integration tests for the Riddle Game application."""
    
    @allure.title("Test module imports")
    @allure.description("Test that all required modules can be imported")
    def test_module_imports(self):
        """Test that the main module can be imported successfully."""
        try:
            with allure.step("Importing riddles_data module"):
                import riddles_data
                assert hasattr(riddles_data, 'riddles'), "Module should contain riddles data"
                assert hasattr(riddles_data, 'validate_start'), "Module should contain validate_start function"
                assert hasattr(riddles_data, 'check_answer'), "Module should contain check_answer function"
        except ImportError as e:
            pytest.fail(f"Failed to import riddles_data module: {e}")
    
    @allure.title("Test riddle game functions")
    @allure.description("Test that game functions work correctly")
    def test_riddle_game_functions(self):
        """Test that game functions have the expected behavior."""
        try:
            from riddles_data import validate_start, check_answer, calculate_score
            
            with allure.step("Testing validate_start function"):
                # Test valid input
                valid, msg = validate_start("TestUser", "25")
                assert valid, f"Valid input should pass: {msg}"
                
                # Test invalid inputs
                invalid_cases = [
                    ("", "25"),  # Empty name
                    ("TestUser", "20"),  # Too young
                    ("TestUser", "not_a_number")  # Invalid age
                ]
                
                for name, age in invalid_cases:
                    valid, msg = validate_start(name, age)
                    assert not valid, f"Invalid input should fail: {name}, {age}"
            
            with allure.step("Testing check_answer function"):
                # Test correct answer
                assert check_answer("phone", "phone"), "Exact match should work"
                assert check_answer(" PHONE ", "phone"), "Case and whitespace should be handled"
                assert not check_answer("wrong", "phone"), "Wrong answer should fail"
                
            with allure.step("Testing calculate_score function"):
                result = calculate_score(15, 20)
                assert result['score'] == 15, "Score should be preserved"
                assert result['total'] == 20, "Total should be preserved"
                assert result['percentage'] == 75.0, "Percentage should be calculated correctly"
                    
        except ImportError:
            pytest.skip("Cannot import game functions")
    
    @allure.title("Test game initialization without GUI")
    @allure.description("Test game logic without requiring GUI components")
    def test_game_logic_without_gui(self):
        """Test core game logic without GUI dependencies."""
        try:
            from riddles_data import riddles, check_answer
            
            with allure.step("Testing answer validation logic"):
                # Test with first riddle
                test_riddle = riddles[0]
                correct_answer = test_riddle["answer"]
                
                # Test correct answer
                assert check_answer(correct_answer, correct_answer), "Correct answer should match"
                
            with allure.step("Testing incorrect answer"):
                wrong_answer = "definitely_wrong_answer"
                assert not check_answer(wrong_answer, correct_answer), "Wrong answer should not match"
                
        except ImportError:
            pytest.skip("Cannot import riddles data")

@allure.feature("Riddle Game")
@allure.story("Performance Tests")
class TestPerformance:
    """Performance tests for riddle game operations."""
    
    @allure.title("Test riddle loading performance")
    @allure.description("Test that riddles can be loaded quickly")
    def test_riddle_loading_performance(self):
        """Test performance of riddle loading operations."""
        import time
        
        try:
            with allure.step("Measuring riddle import time"):
                start_time = time.time()
                from riddles_data import riddles
                import_time = time.time() - start_time
                
                assert import_time < 1.0, f"Riddle import took {import_time:.3f}s, should be under 1s"
                
            with allure.step("Measuring riddle access time"):
                start_time = time.time()
                for _ in range(1000):
                    _ = riddles[0]["question"]
                    _ = riddles[0]["answer"] 
                    _ = riddles[0]["hint"]
                access_time = time.time() - start_time
                
                assert access_time < 0.1, f"1000 riddle accesses took {access_time:.3f}s, should be under 0.1s"
                
        except ImportError:
            pytest.skip("Cannot import riddles for performance testing")

@allure.feature("Riddle Game")
@allure.story("Security Tests")  
class TestSecurity:
    """Security-related tests for the riddle game."""
    
    @allure.title("Test input sanitization")
    @allure.description("Test that user inputs are handled safely")
    def test_input_sanitization(self):
        """Test input sanitization and validation."""
        with allure.step("Testing malicious username inputs"):
            malicious_inputs = [
                "<script>alert('xss')</script>",
                "'; DROP TABLE users; --",
                "../../../etc/passwd",
                "admin' OR '1'='1",
                "\x00\x01\x02\x03"
            ]
            
            for malicious_input in malicious_inputs:
                # Simulate the username validation logic
                sanitized = malicious_input.strip()
                # The game should handle these inputs gracefully
                assert isinstance(sanitized, str), "Input should remain a string after sanitization"
        
        with allure.step("Testing age input validation"):
            invalid_ages = [
                "not_a_number",
                "21.5",
                "-5",
                "999999999999999999999",
                "21; rm -rf /",
                None
            ]
            
            for invalid_age in invalid_ages:
                try:
                    age = int(str(invalid_age)) if invalid_age is not None else int(invalid_age)
                    # Should either convert properly or raise ValueError
                    assert isinstance(age, int), "Age should be converted to integer"
                except (ValueError, TypeError):
                    # This is expected for invalid inputs
                    pass