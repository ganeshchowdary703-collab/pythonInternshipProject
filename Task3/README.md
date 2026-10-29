# Basic Chatbot

A simple rule-based chatbot for the console. It reads your message, looks for known words or phrases, and replies
with a predefined answer.

## Run
```bash
python chatbot.py        # Python 3.8+, no extra packages
python test_chatbot.py   # 8 automated tests
```

## Example
```
Chatty: Hi! I'm Chatty. Type 'bye' to leave, or 'help' for ideas.
You: Hello!
Chatty: Hi!
You: how are you?
Chatty: I'm fine, thanks!
You: what is your name
Chatty: I'm Chatty, a simple chatbot.
You: bye
Chatty: Goodbye!
```

## What it understands
| You say (any case, punctuation ignored) | Bot replies |
|---|---|
| hello, hi, hey, good morning/afternoon/evening | Hi! |
| how are you | I'm fine, thanks! |
| bye, goodbye, exit, quit, see you | Goodbye! (and the chat ends) |
| what is your name, who are you | I'm Chatty, a simple chatbot. |
| thanks, thank you | You're welcome! |
| help | a list of things to try |
| anything else | Sorry, I don't understand that. |

Words are matched as whole words, so "this" does not trigger "hi". If a message contains several rules, the first
matching rule wins (goodbye, then how are you, then greetings), so "hello, how are you?" gets "I'm fine, thanks!".

## Project structure
```
basic_chatbot/
├── chatbot.py        # the chatbot
├── test_chatbot.py   # unittest tests
└── README.md
```

## Concepts demonstrated
| Concept | Where |
|---|---|
| if-elif | `get_reply()` checks the rules in order |
| Functions | `clean`, `has`, `get_reply`, `is_goodbye`, `chat` |
| Loops | `chat()` keeps going until the user says goodbye |
| Input / output | `input("You: ")` and `print` |

## Ideas to extend
Add more rules or a dictionary of replies, random choices among several replies, remember the user's name,
tell the time and date, or save the conversation to a file.
