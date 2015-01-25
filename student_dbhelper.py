from pymongo import MongoClient
from bson.objectid import ObjectId
from validation import *

client = MongoClient()
db = client.gradebook
students = db.students

# TODO email confirmation
def insert(name, email, password):
    response_tuple = isValidName(name)
    if not response_tuple[0]:
        return response_tuple
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
            'name' : name,
            'courses' : []
        }
        students.insert(new_user)
        return (True, "Successfully registered. Enjoy!")
    else:
        return (False, "Error: A user with that email already exists.")

def exists(email, studentId=None):
    if studentId:
        try:
            id = ObjectId(studentId)
            return students.find({'_id' : id}).count() > 0
        except:
            return False
    else:
        return students.find({'email' : email}).count() > 0

def remove(email):
    students.remove({'email' : email}, multi=False)

def get(email, student_id=None):
    if student_id:
        try:
            id = ObjectId(student_id)
            return students.find({'_id': id})
        except:
            return None
    else:
        return students.find({'email': email})

def update(email, studentId=None, new_email=None, name=None, password=None, courses=None):
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
    if(exists(email, studentId)):
        updateDict = {}
        if new_email != None: updateDict['email'] = new_email
        if name != None: updateDict['name'] = name
        if password != None: updateDict['password'] =\
                        generatePasswordHash(password)
        if courses != None: updateDict['courses'] = courses
        if studentId:
            try:
                students.update(
                        {'_id': ObjectId(studentId)},
                        {'$set': updateDict}
                )
            except:
                return (False, "Error: Invalid student id")
        else:
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

def hasCourse(email, courseId, studentId=None,):
    student = get(email, student_id=studentId)
    if student.count() == 1:
        return courseId in student[0]['courses']
    return False

def addCourse(studentId, courseId):
    student = get('', student_id=studentId)
    if student and student.count() == 1:
        student = student[0]
        courses = student['courses']
        if courses:
            courses.append(courseId)
        else:
            courses = [courseId]
        update('', studentId=studentId, courses=courses)

def getId(email):
    student = students.find({'email' : email},
                         {'_id' : 1})
    if student.count() == 1:
        return str(student[0]['_id'])
    else:
        return None

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

