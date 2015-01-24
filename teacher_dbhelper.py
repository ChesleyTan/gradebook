from pymongo import MongoClient
from bson.objectid import ObjectId
from validation import *

client = MongoClient()
db = client.gradebook
teachers = db.teachers

# TODO email confirmation
# TODO check return value for insert
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
            'school' : '',
            'courses' : []
        }
        teachers.insert(new_user)
        return (True, "Successfully registered. Enjoy!")
    else:
        return (False, "Error: A user with that email already exists.")

def exists(email):
    return teachers.find({'email' : email}).count() > 0

def remove(email):
    teachers.remove({'email' : email}, multi=False)

def get(email, teacher_id=None):
    if teacher_id:
        id = ObjectId(teacher_id)
        return teachers.find({'_id': id})
    else:
        return teachers.find({'email': email})

def update(email, new_email=None, name=None, school=None, password=None,
           courses=None):
    if new_email:
        response_tuple = isValidEmail(new_email)
        if not response_tuple[0]:
            return response_tuple
    if name:
        response_tuple = isValidName(name)
        if not response_tuple[0]:
            return response_tuple
    if school:
        response_tuple = isValidSchool(school)
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
    if new_email and new_email != email and exists(new_email):
        return (False, "That email is already taken.")
    if exists(email):
        updateDict = {}
        if new_email: updateDict['email'] = new_email
        if name: updateDict['name'] = name
        if school: updateDict['school'] = school
        if password: updateDict['password'] =\
                             generatePasswordHash(password)
        if courses: updateDict['courses'] = courses
        teachers.update(
            {'email': email},
                {'$set': updateDict}
        )
        return (True, "Successfully updated info.")
    else:
        return (False, "Error: User doesn't exist!")

def addCourseId(email, courseId):
    teacher = teachers.find({'email' : email})
    if teacher.count() == 1:
        courses = teacher[0]['courses']
        courses.append(courseId)
        teachers.update(
            {'email' : email},
            {'$set': {
                'courses' : courses
                }
            }
        )
        return (True, "Sucessfully updated courses.")
    else:
        return (False, "Error: User doesn't exist!")

def removeCourseId(email, courseObjectId):
    teacher = teachers.find({'email' : email})
    if teacher.count() == 1:
        courses = teacher[0]['courses']
        courses.remove(courseObjectId)
        teachers.update(
            {'email' : email},
            {'$set': {
                'courses' : courses
                }
            }
        )
        return (True, "Sucessfully updated courses.")
    else:
        return (False, "Error: User doesn't exist!")

def dump():
    for c in teachers.find():
        print c

def drop():
    teachers.remove()

def validate(email, tryPassword):
    teacher = get(email)
    isValid = teacher.count() != 0
    if isValid:
        isValid = checkPassword(teacher[0]['password'], tryPassword)
        if isValid:
            return (True, "Successfully logged in!")
    return (False, "Email or password is incorrect.")

########## TESTING ##########
if __name__ == "__main__":
    drop()
    response_tuple = insert("john@gmail.com", "p4$$w0rD", "John Doe",
                            "Stuyvesant High School")
    if not response_tuple[0]:
        print response_tuple[1]
    dump()
    response_tuple = update("john@gmail.com", name="Anonymous",
                            new_email="anonymous@gmail.com",
                            school="Hogwarts School of Witchcraft and Wizardry",
                            password="thisislongerthan6characters")
    if not response_tuple[0]:
        print response_tuple[1]
    dump()

