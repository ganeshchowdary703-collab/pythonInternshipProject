"""Automated tests:  python test_chatbot.py"""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import chatbot


class TestReplies(unittest.TestCase):
    def test_required_examples(self):
        self.assertEqual(chatbot.get_reply("hello"), "Hi!")
        self.assertEqual(chatbot.get_reply("how are you"), "I'm fine, thanks!")
        self.assertEqual(chatbot.get_reply("bye"), "Goodbye!")

    def test_case_and_punctuation_ignored(self):
        self.assertEqual(chatbot.get_reply("  HELLO!!! "), "Hi!")
        self.assertEqual(chatbot.get_reply("How are you?"), "I'm fine, thanks!")
        self.assertEqual(chatbot.get_reply("Bye."), "Goodbye!")

    def test_whole_word_matching(self):
        self.assertNotEqual(chatbot.get_reply("this is nice"), "Hi!")     # 'hi' inside 'this'
        self.assertNotEqual(chatbot.get_reply("whip"), "Hi!")

    def test_combined_message(self):
        self.assertEqual(chatbot.get_reply("hello, how are you?"), "I'm fine, thanks!")
        self.assertEqual(chatbot.get_reply("ok thanks bye"), "Goodbye!")

    def test_other_rules(self):
        self.assertIn(chatbot.BOT_NAME, chatbot.get_reply("what is your name"))
        self.assertEqual(chatbot.get_reply("thank you"), "You're welcome!")
        self.assertIn("hello", chatbot.get_reply("help"))

    def test_empty_and_unknown(self):
        self.assertIn("type something", chatbot.get_reply("   "))
        self.assertIn("don't understand", chatbot.get_reply("purple elephants"))


class TestChatLoop(unittest.TestCase):
    def run_chat(self, inputs):
        out = io.StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(out):
            chatbot.chat()
        return out.getvalue()

    def test_loop_ends_on_goodbye(self):
        out = self.run_chat(["hello", "how are you", "bye"])
        self.assertIn("Hi!", out)
        self.assertIn("I'm fine, thanks!", out)
        self.assertIn("Goodbye!", out)

    def test_loop_continues_until_goodbye(self):
        # if the loop stopped early, the fourth scripted input would never be read
        # and the unused inputs would not raise - so check the reply order instead
        out = self.run_chat(["hello", "blah", "thanks", "quit"])
        self.assertLess(out.index("Hi!"), out.index("don't understand"))
        self.assertLess(out.index("don't understand"), out.index("You're welcome!"))
        self.assertTrue(out.strip().endswith("Goodbye!"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
