from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash

def isValidEmail(email):
    valid = validate_email(email)
    if valid:
        return (True, "Successfully validated email")
    else:
        return (False, "Error: Invalid email")

def isValidName(name):
    valid = len(name) < 31
    if not valid:
        return (False, "Error: Name is too long (Greater than 30 characters)")
    valid = len(name) > 0
    if not valid: return (False, "Error: Name is too short (Fewer than 1 character)")
    return (True, "Successfully validated name")

def isValidPassword(password):
    valid = len(password) < 51
    if not valid:
        return (False, "Error: Password is too long (Greater than 50 characters)")
    valid = len(password) > 5
    if not valid:
        return (False, "Error: Password is too short (Fewer than 6 characters)")
    return (True, "Successfully validated password")

def isValidSchool(school):
    valid = len(school) > 0
    if not valid:
        return (False, "Error: Name of school is too short (Fewer than 1"
                " character)")
    valid = len(school) < 101
    if not valid:
        return (False, "Error: Name of school is too long (Greater than 100"
                " characters)")
    valid = school[0].isupper()
    if not valid:
        return (False, "Error: Name of school must be capitalized")
    return (True, "Successfully validated school name")

def isValidClass(className):
    valid = len(className) > 1
    if not valid:
        return (False, "Error: Name of class is too short (Fewer than 2"
                " characters)")
    valid = len(className) < 31
    if not valid:
        return (False, "Error: Name of class is too long (Greater than 30"
                " characters)")
    return (True, "Successfully validated class name")

def isValidDescription(description):
    valid = len(description) < 301
    if not valid:
        return (False, "Error: Description is too long (Greater than 300"
                " characters)")
    return (True, "Successfully validated description")

def checkPassword(hashedPassword, tryPassword):
    return check_password_hash(hashedPassword, tryPassword)

def generatePasswordHash(password):
    return generate_password_hash(password)
