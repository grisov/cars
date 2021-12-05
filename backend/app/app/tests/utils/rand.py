import random
import string


def random_lower_string() -> str:
    """Generate a string of 32 random lowercase Latin letters."""
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    """Generate a random email address."""
    return f"{random_lower_string()}@{random_lower_string()}.{random.choice(('com', 'net', 'biz', 'info', 'name', 'eu', 'ua'))}"
