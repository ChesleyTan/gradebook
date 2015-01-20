from pymongo import MongoClient
from validation import *

client = MongoClient()
db = client.gradebook
teachers = db.teachers

# TODO email confirmation
def insert(email, password, name, school):
    response_tuple = isValidEmail(email)
    if not response_tuple[0]:
        return response_tuple
    response_tuple = isValidPassword(password)
    if not response_tuple[0]:
        return response_tuple
    response_tuple = isValidName(name)
    if not response_tuple[0]:
        return response_tuple
    response_tuple = isValidSchool(school)
    if not response_tuple[0]:
        return response_tuple
    if (not exists(email)):
        new_user = {
            'email' : email,
            'password' : generatePasswordHash(password),
            'name' : name,
            'school' : school,
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

def get(email):
    return teachers.find({'email': email})

def update(email, new_email=None, name=None, school=None, password=None,
           courses=None):
    if new_email:
        response_tuple = isValidEmail(new_email)
        if not response_tuple[0]:
            return response_tuple
    if password:
        response_tuple = isValidPassword(password)
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
    if(exists(email)):
        updateDict = {}
        if new_email != None: updateDict['email'] = new_email
        if name != None: updateDict['name'] = name
        if school != None: updateDict['school'] = school
        if password != None: updateDict['password'] =\
                             generatePasswordHash(password)
        if courses != None: updateDict['courses'] = courses
        teachers.update(
            {'email': email},
                {'$set': updateDict}
        )
        return "Successfully updated info."
    else:
        return "Error: User doesn't exist!"

def dump():
    for c in teachers.find():
        print c

def drop():
    teachers.remove()

########## TESTING ##########
if __name__ == "__main__":
    drop()
    response_tuple = insert("john@gmail.com", "p4$$w0rD", "John Doe",
                            "Stuyvesant High School")
    if not response_tuple[0]:
        print response_tuple[1]
    dump()
    update("john@gmail.com", name="Anonymous", new_email="anonymous@gmail.com",
            school="Hogwarts School of Witchcraft and Wizardry")
    dump()

