from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash
import time
from datetime import date

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

def isValidCourse(course):
    valid = len(course) > 1
    if not valid:
        return (False, "Error: Name of course is too short (Fewer than 2"
                " characters)")
    valid = len(course) < 101
    if not valid:
        return (False, "Error: Name of course is too long (Greater than 100"
                " characters)")
    return (True, "Successfully validated course name")

def isValidCourseDescription(description):
    valid = len(description) < 301
    if not valid:
        return (False, "Error: Description is too long (Greater than 300"
                " characters)")
    return (True, "Successfully validated description")

def isValidAssignment(assignment):
    valid = len(assignment) > 1
    if not valid:
        return (False, "Error: Name of assignment is too short (Fewer than 2"
                " characters)")
    valid = len(assignment) < 101
    if not valid:
        return (False, "Error: Name of assignment is too long (Greater than 100"
                " characters)")
    return (True, "Successfully validated assignment name")

def isValidAssignmentDescription(description):
    valid = len(description) < 1001
    if not valid:
        return (False, "Error: Description is too long (Greater than 1000"
                " characters)")
    return (True, "Successfully validated description")

def isValidDueDate(dueDate):
    valid = date.today() < dueDate
    if not valid:
        return (False, "Error: Due date cannot be in the past")
    return (True, "Successfully validated due date")

def isValidAssignmentType(aType):
    if not (aType=='warning' or\
       aType=='' or\
       aType=='info'):
        return (False, "Invalid assignment type")
    return (True, "Successfully validated assignment type")
        

def checkPassword(hashedPassword, tryPassword):
    return check_password_hash(hashedPassword, tryPassword)

def generatePasswordHash(password):
    return generate_password_hash(password)
