import random

QUOTES = [
    "I am inevitable.",
    "Perfectly balanced, as all things should be.",
    "The hardest choices require the strongest wills.",
    "You could not live with your own failure. Where did that bring you? Back to me.",
    "Dread it. Run from it. Destiny arrives all the same.",
    "I know what it's like to lose. To feel so desperately that you're right... yet to fail nonetheless.",
    "I ignored my destiny once. I cannot do that again. Even for you.",
]

_rng = random.SystemRandom()

def random_quote() -> str:
    return _rng.choice(QUOTES)
