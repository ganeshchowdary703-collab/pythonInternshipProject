# Hangman (console game)

A simple text-based Hangman game. The computer picks a secret word and you guess it one letter at a time.
Six wrong guesses and you lose.

## Run
```bash
python hangman.py          # needs Python 3.8+, no extra packages
python test_hangman.py     # run the automated tests (13 tests)
```

## Rules
* The secret word is chosen at random from 5 predefined words: `python, hangman, keyboard, internet, developer`.
* Enter one letter per turn (upper or lower case both work).
* You may guess wrong **6 times**; each wrong guess draws another part of the hangman.
* Guess every letter before the drawing is finished and you win.
* Invalid input (numbers, symbols, several letters) and repeated letters are **not** counted as wrong guesses.
* After each game you can play again; the score is tracked while the program runs.

## Project structure
```
hangman_game/
├── hangman.py        # the game
├── test_hangman.py   # automated tests (unittest, scripted keyboard input)
└── README.md
```

## How the code works
| Part | Concept it demonstrates |
|---|---|
| `WORDS` list, `STAGES` list (7 ASCII pictures) | **lists** |
| `choose_word()` uses `random.choice` | **random** |
| `play_round()` loops while wrong guesses < 6 and word not complete | **while loop** |
| Branching on error / repeated / correct / wrong guess | **if-else** |
| `build_display()`, `check_guess()` (strip, lower, isalpha, len) | **strings** |

Functions are kept small (`choose_word`, `build_display`, `check_guess`, `is_won`, `show_status`, `play_round`, `main`)
so each one can be tested on its own.

## Ideas to extend
Add more words or categories, a difficulty setting (fewer allowed misses), a hint option, a "guess the whole word" option,
or load words from a file.
