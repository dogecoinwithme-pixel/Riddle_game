"""
Test configuration and fixtures for the Riddle Game tests.
"""
import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def riddles_data():
    """Fixture to provide riddles data for testing."""
    return [
        {"question": "What's always hard to keep in your pants when you're excited?", "answer": "phone", "hint": "It's something you check often."},
        {"question": "What grows bigger the more you play with it?", "answer": "ego", "hint": "It's inflated by compliments."},
        {"question": "What's slippery when wet and hard to hold onto?", "answer": "soap", "hint": "It's used in the shower."},
    ]

@pytest.fixture
def sample_game_data():
    """Fixture to provide sample game data for testing."""
    return {
        "username": "TestUser",
        "age": 25,
        "score": 0,
        "riddle_index": 0
    }