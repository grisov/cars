import pytest
import re
from app.tests.utils import random_lower_string, random_email, random_plate_number


@pytest.mark.parametrize("execution_number", range(100))
def test_random_lower_string(execution_number: int) -> None:
    """Function that generates a string of a given length consisting of lowercase letters."""
    string = random_lower_string()
    assert isinstance(string, str), "Instance of the string type"
    assert string.isalpha(), "Consists only of letters"
    assert string.islower(), "Only lower letters"
    assert len(string) == 32, "Fixed length string"


@pytest.mark.parametrize("execution_number", range(100))
def test_random_email(execution_number: int) -> None:
    """Function that generates a random email address."""
    string = random_email()
    assert isinstance(string, str), "Instance of the string type"
    assert re.match(r"^[a-z]{32}@[a-z]{32}\.[a-z]{2,5}$", string), "Corresponds to the regular expression"
    assert string.islower(), "Only lower letters"
    assert len(string) >= 32 * 2 + 4, "Fixed length string"


@pytest.mark.parametrize("execution_number", range(100))
def test_random_plate_number(execution_number: int) -> None:
    """Function that generates a random plate number of the vehicle."""
    string = random_plate_number()
    assert isinstance(string, str), "Instance of the string type"
    assert re.match(r"^[A-Z]{2}\s[0-9]{4}\s[A-Z]{2}$", string), "Corresponds to the regular expression"
    assert len(string) == 10, "Fixed length string"
