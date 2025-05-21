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
    length = level + 2  # base 3 length increasing by 1 each level
    if seq_type == "Numbers":
        return [random.choice(NUMBER_WORDS) for _ in range(length)]
    else:
        return [random.choice(COMMON_WORDS) for _ in range(length)]
