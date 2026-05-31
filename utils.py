"""
Utility functions for NUQRO:
- Shuffle answer options to remove order bias.
- Progress bar display.
- Improved timed input with proper cancellation.
"""

import random
import threading
import time
import sys

def shuffle_question_options(question):
    """
    Take a question dict with 'options' (A,B,C,D) and return:
        shuffled_options: dict with letters A-D in new order
        answer_mapping: dict mapping new letter -> original letter
    """
    items = list(question['options'].items())  # [('A', 'text'), ('B', 'text'), ...]
    random.shuffle(items)
    shuffled_options = {}
    mapping = {}
    for new_idx, (orig_letter, text) in enumerate(items):
        new_letter = chr(65 + new_idx)   # A, B, C, D
        shuffled_options[new_letter] = text
        mapping[new_letter] = orig_letter
    return shuffled_options, mapping

def apply_shuffle_to_answers(user_ans, mapping):
    """Convert user's answer (new letter) back to original letter."""
    return mapping.get(user_ans, user_ans)

def progress_bar(current, total, width=30):
    """Return a string like '[██████░░░░░░░░░░░░] 7/10'"""
    filled = int(round((current / total) * width))
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {current}/{total}"

def timed_input(prompt, time_limit, default_on_timeout=""):
    """
    Show prompt and wait for input with a countdown timer.
    Uses threading.Event for clean cancellation.
    Returns user input (stripped) or default_on_timeout if timeout.
    """
    user_input = [default_on_timeout]
    event = threading.Event()

    def get_input():
        try:
            user_input[0] = input(prompt)
        except EOFError:
            user_input[0] = default_on_timeout
        finally:
            event.set()

    thread = threading.Thread(target=get_input)
    thread.daemon = True
    thread.start()

    for remaining in range(time_limit, 0, -1):
        if event.is_set():
            break
        sys.stdout.write(f"\r  ⏱️ Time left: {remaining}s ")
        sys.stdout.flush()
        time.sleep(1)

    if not event.is_set():
        print(f"\r  ⏱️ Time left: 0s  - Time's up! Skipping.")
        return default_on_timeout
    else:
        print("\r" + " " * 30 + "\r", end="")
        return user_input[0].strip()
    