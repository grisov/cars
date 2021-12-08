import random
import string


def random_lower_string() -> str:
    """Generate a string of 32 random lowercase Latin letters."""
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    """Generate a random email address."""
    return f"{random_lower_string()}@{random_lower_string()}.{random.choice(('com', 'net', 'biz', 'info', 'name', 'eu', 'ua'))}"


def random_plate_number() -> str:
    """Generate a random plate number of the vehicle."""
    return "{prefix} {number} {suffix}".format(
        prefix=random_lower_string()[:2].upper(),
        number=random.randint(1000, 9999),
        suffix=random_lower_string()[:2].upper()
    )
