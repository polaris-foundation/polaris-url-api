import random
import string
from typing import List

# Allow any lowercase character or digit, except for the below.
ALLOWED_CHARS: List[str] = list(
    set(string.ascii_lowercase + string.digits) - {"o", "l", "0", "1", "i"}
)


def generate_secure_random_string(length: int = 10) -> str:
    if length < 3:
        raise ValueError("Cannot generate a secure random string of length < 3")
    return "".join([random.choice(ALLOWED_CHARS) for _ in range(length)])
