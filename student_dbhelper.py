from pymongo import MongoClient
from bson.objectid import ObjectId
from validation import *

client = MongoClient()
db = client.gradebook
students = db.students

# TODO email confirmation
def insert(email, password):
    response_tuple = isValidEmail(email)
    if not response_tuple[0]:
        return response_tuple
    response_tuple = isValidPassword(password)
    if not response_tuple[0]:
        return response_tuple
    if (not exists(email)):
        new_user = {
            'email' : email,
            'password' : generatePasswordHash(password),
            'name' : '',
            'courses' : []
        }
        students.insert(new_user)
        return (True, "Successfully registered. Enjoy!")
    else:
        return (False, "Error: A user with that email already exists.")

def exists(email):
    return students.find({'email' : email}).count() > 0

def remove(email):
    students.remove({'email' : email}, multi=False)

def get(email, student_id=None):
    if student_id:
        id = ObjectId(student_id)
        return students.find({'_id': id})
    else:
        return students.find({'email': email})

def update(email, new_email=None, name=None, password=None, courses=None):
    if new_email:
        response_tuple = isValidEmail(new_email)
        if not response_tuple[0]:
            return response_tuple
    if name:
        response_tuple = isValidName(name)
        if not response_tuple[0]:
            return response_tuple
    if password:
        response_tuple = isValidPassword(password)
        if not response_tuple[0]:
            return response_tuple
    if courses:
        for course in courses:
            response_tuple = isValidCourse(course)
            if not response_tuple[0]:
                return response_tuple
    if(exists(email)):
        updateDict = {}
        if new_email: updateDict['email'] = new_email
        if name: updateDict['name'] = name
        if password: updateDict['password'] =\
                        generatePasswordHash(password)
        if courses: updateDict['courses'] = courses
        students.update(
                {'email': email},
                {'$set': updateDict}
        )
        return (True, "Successfully updated info.")
    else:
        return (False, "Update info error: User doesn't exist!")

def dump():
    for c in students.find():
        print c

def drop():
    students.remove()

def validate(email, tryPassword):
    student = get(email)
    isValid = student.count() == 1
    if isValid:
        isValid = checkPassword(student[0]['password'], tryPassword)
        if isValid:
            return (True, "Successfully logged in!")
    return (False, "Email or password is incorrect.")

def hasCourse(email, courseId):
    student = get(email)
    if student.count() == 1:
        return courseId in student[0]['courses']
    return False

########## TESTING ##########
if __name__ == "__main__":
    drop()
    response_tuple = insert("john@gmail.com", "p4$$w0rD", "John Doe")
    if not response_tuple[0]:
        print response_tuple[1]
    dump()
    response_tuple = update("john@gmail.com", name="Anonymous",
                            new_email="anonymous@gmail.com",
                            password="you'llneverguessthispassword")
    if not response_tuple[0]:
        print response_tuple[1]
    dump()

