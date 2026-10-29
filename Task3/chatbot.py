"""
Basic rule-based chatbot.

The bot reads what you type, looks for known words or phrases, and answers with a predefined reply.
Type "bye" to end the chat.

Concepts used: if-elif, functions, loops, input/output.
Run it with:  python chatbot.py
"""
import string

BOT_NAME = "Chatty"


def clean(text):
    """Lowercase the message, remove punctuation and extra spaces: 'Hello!!' -> 'hello'."""
    text = text.lower().strip()
    for ch in string.punctuation:
        text = text.replace(ch, " ")
    return " ".join(text.split())


def has(text, phrases):
    """True if any phrase appears in the text as whole words (so 'hi' does not match 'this')."""
    padded = f" {text} "
    for phrase in phrases:
        if f" {phrase} " in padded:
            return True
    return False


def get_reply(message):
    """Return the bot's reply to one message. The order of the checks matters."""
    text = clean(message)

    if text == "":
        return "Please type something and I'll reply."
    elif has(text, ["bye", "goodbye", "exit", "quit", "see you"]):
        return "Goodbye!"
    elif has(text, ["how are you", "how are you doing", "how do you do", "hows it going"]):
        return "I'm fine, thanks!"
    elif has(text, ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hi!"
    elif has(text, ["your name", "who are you"]):
        return f"I'm {BOT_NAME}, a simple chatbot."
    elif has(text, ["thanks", "thank you"]):
        return "You're welcome!"
    elif has(text, ["help", "what can you do"]):
        return "Try saying: hello, how are you, what is your name, thanks, or bye."
    else:
        return "Sorry, I don't understand that. Type 'help' to see what I can do."


def is_goodbye(message):
    return has(clean(message), ["bye", "goodbye", "exit", "quit", "see you"])


def chat():
    """Main loop: keep chatting until the user says goodbye."""
    print(f"{BOT_NAME}: Hi! I'm {BOT_NAME}. Type 'bye' to leave, or 'help' for ideas.")
    chatting = True
    while chatting:
        message = input("You: ")
        print(f"{BOT_NAME}: {get_reply(message)}")
        if is_goodbye(message):
            chatting = False


if __name__ == "__main__":
    try:
        chat()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{BOT_NAME}: Goodbye!")
