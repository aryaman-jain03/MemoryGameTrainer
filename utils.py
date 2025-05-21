# utils.py

import random

NUMBER_WORDS = [str(n) for n in range(10)]

COMMON_WORDS = [
    "apple", "brain", "cloud", "dance", "eagle",
    "flower", "ghost", "happy", "island", "jelly",
    "kite", "lemon", "music", "night", "orange",
    "piano", "queen", "river", "star", "tree",
    "umbrella", "violet", "water", "xray", "yellow", "zebra"
]

def generate_sequence(level, seq_type):
    """
    Generates a list of numbers or words based on the current level and sequence type.

    Parameters:
    - level (int): The current level of the game.
    - seq_type (str): Either "Numbers" or "Words".

    Returns:
    - List[str]: A sequence to memorize.
    """
    length = min(level + 2, 20)  # Cap length for playability
    if seq_type == "Numbers":
        return random.choices(NUMBER_WORDS, k=length)
    else:
        return random.sample(COMMON_WORDS, k=length if length <= len(COMMON_WORDS) else len(COMMON_WORDS))
