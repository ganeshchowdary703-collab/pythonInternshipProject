"""
Hangman - a simple text-based word guessing game.

The computer picks a secret word from a list of 5 predefined words and the player guesses it
one letter at a time. Six wrong guesses and the player loses.

Concepts used: random, while loops, if-else, strings, lists.
Run it with:  python hangman.py
"""
import random

# ----------------------------------------------------------------------------- settings
WORDS = ["python", "hangman", "keyboard", "internet", "developer"]   # the 5 predefined words
MAX_WRONG = 6                                                        # incorrect guesses allowed

# One picture per number of wrong guesses (0 to 6)
STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========""",
]


# ----------------------------------------------------------------------------- helpers
def choose_word():
    """Pick a random secret word from the list."""
    return random.choice(WORDS)


def build_display(word, guessed):
    """Return the word with unguessed letters hidden, e.g. 'p _ t _ _ n'."""
    shown = []
    for letter in word:
        if letter in guessed:
            shown.append(letter)
        else:
            shown.append("_")
    return " ".join(shown)


def check_guess(raw):
    """Validate the player's input. Returns (letter, error_message); one of them is None."""
    text = raw.strip().lower()
    if len(text) != 1:
        return None, "Please enter exactly ONE letter."
    if not text.isalpha():
        return None, "Letters only (a-z), no numbers or symbols."
    return text, None


def is_won(word, guessed):
    """True when every letter of the word has been guessed."""
    for letter in word:
        if letter not in guessed:
            return False
    return True


def show_status(word, guessed, wrong):
    """Print the gallows, the hidden word and the letters tried so far."""
    print(STAGES[len(wrong)])
    print("\nWord:  ", build_display(word, guessed))
    print("Wrong: ", " ".join(wrong) if wrong else "-")
    print(f"Guesses left: {MAX_WRONG - len(wrong)}")


# ----------------------------------------------------------------------------- game
def play_round(word=None):
    """Play one game. Returns True if the player won, False if they lost."""
    if word is None:
        word = choose_word()
    guessed = []      # correct letters
    wrong = []        # incorrect letters

    print("\n" + "=" * 36)
    print(f"New game! The word has {len(word)} letters.")

    while len(wrong) < MAX_WRONG and not is_won(word, guessed):
        show_status(word, guessed, wrong)
        letter, error = check_guess(input("\nGuess a letter: "))

        if error:
            print(error)
        elif letter in guessed or letter in wrong:
            print(f"You already tried '{letter}'. Try a different letter.")
        elif letter in word:
            guessed.append(letter)
            print(f"Good guess! '{letter}' is in the word.")
        else:
            wrong.append(letter)
            print(f"Sorry, '{letter}' is not in the word.")

    show_status(word, guessed, wrong)
    if is_won(word, guessed):
        print(f"\nYou won! The word was '{word}'.")
        return True
    print(f"\nGame over! The word was '{word}'.")
    return False


def main():
    wins, games = 0, 0
    print("Welcome to HANGMAN!")
    print(f"Guess the secret word one letter at a time. You may miss {MAX_WRONG} times.")

    playing = True
    while playing:
        games += 1
        if play_round():
            wins += 1
        print(f"Score: {wins} won out of {games} game(s).")
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            playing = False
    print("Thanks for playing. Goodbye!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame ended. Goodbye!")
