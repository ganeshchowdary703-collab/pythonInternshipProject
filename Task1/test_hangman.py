"""Automated tests:  python test_hangman.py"""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import hangman


def play(word, inputs):
    """Run one round with scripted keyboard input; return (won, printed_output)."""
    out = io.StringIO()
    with patch("builtins.input", side_effect=inputs), redirect_stdout(out):
        won = hangman.play_round(word)
    return won, out.getvalue()


class TestHelpers(unittest.TestCase):
    def test_word_list_has_five_words(self):
        self.assertEqual(len(hangman.WORDS), 5)

    def test_choose_word_is_from_list(self):
        for _ in range(50):
            self.assertIn(hangman.choose_word(), hangman.WORDS)

    def test_one_stage_picture_per_wrong_guess(self):
        self.assertEqual(len(hangman.STAGES), hangman.MAX_WRONG + 1)

    def test_build_display(self):
        self.assertEqual(hangman.build_display("python", []), "_ _ _ _ _ _")
        self.assertEqual(hangman.build_display("python", ["p", "o"]), "p _ _ _ o _")

    def test_check_guess_validation(self):
        self.assertEqual(hangman.check_guess(" A "), ("a", None))
        for bad in ["", "ab", "5", "!", "  "]:
            letter, err = hangman.check_guess(bad)
            self.assertIsNone(letter)
            self.assertTrue(err)

    def test_is_won(self):
        self.assertTrue(hangman.is_won("aab", ["a", "b"]))
        self.assertFalse(hangman.is_won("aab", ["a"]))


class TestGameplay(unittest.TestCase):
    def test_win(self):
        won, out = play("python", list("python"))
        self.assertTrue(won)
        self.assertIn("You won", out)

    def test_lose_after_six_wrong_guesses(self):
        won, out = play("python", list("qwzxcv"))
        self.assertFalse(won)
        self.assertIn("Game over", out)
        self.assertIn("'python'", out)

    def test_exactly_six_wrong_guesses_allowed(self):
        won, _ = play("python", list("qwzxc") + list("python"))     # 5 wrong, then win
        self.assertTrue(won)

    def test_repeated_guess_is_not_penalised(self):
        won, out = play("python", ["q", "q", "q", "q", "q", "q", "q"] + list("python"))
        self.assertTrue(won)                                        # only 1 wrong guess was counted
        self.assertIn("already tried", out)

    def test_invalid_input_is_not_penalised(self):
        won, out = play("python", ["1", "", "ab", "!"] + list("python"))
        self.assertTrue(won)
        self.assertIn("exactly ONE letter", out)
        self.assertIn("Letters only", out)

    def test_uppercase_input_works(self):
        won, _ = play("python", list("PYTHON"))
        self.assertTrue(won)

    def test_main_replay_and_score(self):
        out = io.StringIO()
        inputs = list("python") + ["y"] + list("qwzxcv") + ["n"]
        with patch("hangman.choose_word", return_value="python"), \
             patch("builtins.input", side_effect=inputs), redirect_stdout(out):
            hangman.main()
        self.assertIn("Score: 1 won out of 1", out.getvalue())
        self.assertIn("Score: 1 won out of 2", out.getvalue())
        self.assertIn("Goodbye", out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
