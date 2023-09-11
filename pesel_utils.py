# pesel_utils.py

import random
import string
import datetime

# Function to remove separators and convert the number to uppercase
def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    if isinstance(number, str):
        return ''.join(filter(str.isdigit, number)).strip()
    else:
        return str(number).strip()

# Function to extract the birth date from the number
def get_birth_date(number):
    number = compact(number)
    year = int(number[0:2])
    month = int(number[2:4])
    day = int(number[4:6])
    year += {
        0: 1900,
        1: 2000,
        2: 2100,
        3: 2200,
        4: 1800,
    }[month // 20]
    month = month % 20
    try:
        return datetime.date(year, month, day)
    except ValueError:
        raise InvalidComponent()

# Function to determine the gender
def get_gender(number):
    number = compact(number)
    if number[9] in '02468':
        return 'F'
    else:
        return 'M'

# Function to calculate the check digit for organizations
def calc_check_digit(number):
    weights = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
    check = sum(w * int(n) for w, n in zip(weights, number))
    return str((10 - check) % 10)

# Function to validate the number
def validate(number):
    number = compact(number)
    if not number.isdigit() or len(number) != 11:
        raise InvalidFormat()
    if number[-1] != calc_check_digit(number[:-1]):
        raise InvalidChecksum()
    get_birth_date(number)
    return number

# Function to check if the number is a valid national identification number
def is_valid(number):
    try:
        number = compact(number.strip("'"))
        if not number.isdigit() or len(number) != 11:
            raise InvalidFormat()
        if number[-1] != calc_check_digit(number[:-1]):
            raise InvalidChecksum()
        get_birth_date(number)
        return True
    except ValidationError:
        return False

# Function to rotate each character in the identifier according to the specified rules
def rotate_identifier(identifier):
    if len(identifier) != 11:
        raise ValueError("Invalid identifier length. It must be 11 characters.")
    rotated_identifier = [(int(char) - 7) % 10 if char.isdigit() else char for char in identifier]
    return "".join(map(str, rotated_identifier))

# Function to convert the current date to a letter representation
def date_to_letters():
    current_date = datetime.datetime.now()
    date_str = current_date.strftime("%Y%m")
    mapping = {str(i): chr(65 + i) for i in range(10)}
    date_letters = ''.join(mapping.get(char, char) for char in date_str)
    return date_letters

# Function to format the rotated identifier with separators, prefix, and suffix
def format_pesel(rotated_pesel):
    mapping = {str(i): chr(65 + i) for i in range(10)}
    letter_pesel = "".join(mapping.get(digit, digit) for digit in rotated_pesel)
    groups = [letter_pesel[i:i + 2] for i in range(0, len(letter_pesel), 2)]
    formatted_pesel = [random.choice(string.ascii_uppercase + string.digits) for _ in range(20)]
    for i, group in enumerate(groups):
        formatted_pesel[i * 3] = group[0]
        if len(group) > 1:
            formatted_pesel[i * 3 + 1] = group[1]
    return "".join(formatted_pesel)
