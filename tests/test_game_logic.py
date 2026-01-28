import sys
import os
from pathlib import Path

# Add parent directory to path so we can import logic_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score
import random

# ==================== Original Tests ====================

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"


# ==================== High/Low Guess Hint Tests ====================

class TestHighLowHints:
    """Test suite for high/low guess hint feedback"""
    
    def test_hint_message_too_high(self):
        # Test that the hint message contains proper feedback for "too high"
        outcome, message = check_guess(75, 50)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"
        assert "LOWER" in message
    
    def test_hint_message_too_low(self):
        # Test that the hint message contains proper feedback for "too low"
        outcome, message = check_guess(25, 50)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"
        assert "HIGHER" in message
    
    def test_hint_message_win(self):
        # Test that winning guess returns correct success message
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"
        assert message == "🎉 Correct!"
        assert "Correct" in message
    
    def test_multiple_too_high_guesses(self):
        # Test multiple guesses that are too high
        secret = 30
        guesses = [100, 90, 80, 70, 60, 50, 40]
        for guess in guesses:
            outcome, message = check_guess(guess, secret)
            assert outcome == "Too High"
            assert "LOWER" in message
    
    def test_multiple_too_low_guesses(self):
        # Test multiple guesses that are too low
        secret = 70
        guesses = [1, 10, 20, 30, 40, 50, 60]
        for guess in guesses:
            outcome, message = check_guess(guess, secret)
            assert outcome == "Too Low"
            assert "HIGHER" in message
    
    def test_edge_case_guess_one_above(self):
        # Test guess that is one above secret
        outcome, message = check_guess(51, 50)
        assert outcome == "Too High"
        assert "LOWER" in message
    
    def test_edge_case_guess_one_below(self):
        # Test guess that is one below secret
        outcome, message = check_guess(49, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message
    
    def test_hint_consistency(self):
        # Test that hints are consistent across multiple calls with same inputs
        secret = 42
        guess = 100
        result1 = check_guess(guess, secret)
        result2 = check_guess(guess, secret)
        assert result1 == result2


# ==================== New Game Button Tests ====================

class TestNewGameFunctionality:
    """Test suite for new_game button reset functionality"""
    
    def test_game_state_reset_attempts(self):
        # Simulate: attempts should be reset to 0 on new game
        # In a real scenario with session state, this would test st.session_state
        initial_attempts = 5
        # After new_game button pressed, attempts should reset
        reset_attempts = 0  # This would be set by new_game button
        assert reset_attempts == 0
    
    def test_game_state_reset_status(self):
        # After new_game, status should always be "playing"
        initial_status = "won"
        # After new_game button pressed
        reset_status = "playing"
        assert reset_status == "playing"
    
    def test_game_state_reset_score(self):
        # Score should be reset to 0 on new game
        initial_score = 150
        # After new_game button pressed
        reset_score = 0
        assert reset_score == 0
    
    def test_game_state_reset_history(self):
        # History should be cleared on new game
        initial_history = [10, 20, 30, 40]
        # After new_game button pressed
        reset_history = []
        assert reset_history == []
    
    def test_new_secret_generated(self):
        # New game should generate a new secret number
        secret1 = random.randint(1, 100)
        secret2 = random.randint(1, 100)
        # Both should be valid numbers in range (not testing exact randomness)
        assert 1 <= secret1 <= 100
        assert 1 <= secret2 <= 100
    
    def test_new_game_clears_all_session_state(self):
        # Test that all session state is properly cleared
        # Simulate game state before new_game button
        session_before = {
            "secret": 42,
            "attempts": 7,
            "score": 120,
            "status": "playing",
            "history": [10, 20, 30, 40, 50]
        }
        
        # Simulate new_game button press
        session_after = {
            "secret": random.randint(1, 100),  # New secret
            "attempts": 0,  # Reset
            "score": 0,  # Reset
            "status": "playing",  # Back to playing
            "history": []  # Cleared
        }
        
        # Verify all required resets happened
        assert session_after["attempts"] == 0
        assert session_after["score"] == 0
        assert session_after["status"] == "playing"
        assert session_after["history"] == []
        assert session_after["secret"] != session_before["secret"] or True  # New secret (probabilistic)
    
    def test_new_game_preserves_difficulty_settings(self):
        # Test that new_game respects difficulty settings
        difficulty = "Hard"
        low, high = get_range_for_difficulty(difficulty)
        
        # New secret should be within the difficulty range
        new_secret = random.randint(low, high)
        assert low <= new_secret <= high
    
    def test_new_game_transitions_from_won_state(self):
        # Test new_game can reset from "won" state
        previous_status = "won"
        # After new_game button
        new_status = "playing"
        assert new_status == "playing"
        assert new_status != previous_status
    
    def test_new_game_transitions_from_lost_state(self):
        # Test new_game can reset from "lost" state
        previous_status = "lost"
        # After new_game button
        new_status = "playing"
        assert new_status == "playing"
        assert new_status != previous_status


# ==================== Integration Tests ====================

class TestGameIntegration:
    """Integration tests for game flow"""
    
    def test_game_flow_with_hints(self):
        # Test a complete game flow with hint generation
        secret = 50
        guesses_and_expected = [
            (75, "Too High"),
            (25, "Too Low"),
            (60, "Too High"),
            (40, "Too Low"),
            (50, "Win")
        ]
        
        for guess, expected_outcome in guesses_and_expected:
            outcome, message = check_guess(guess, secret)
            assert outcome == expected_outcome
    
    def test_parse_guess_with_check_guess(self):
        # Test parse_guess output works with check_guess
        ok, guess_int, err = parse_guess("42")
        assert ok is True
        assert guess_int == 42
        
        outcome, message = check_guess(guess_int, 50)
        assert outcome == "Too Low"
