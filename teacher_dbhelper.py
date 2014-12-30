from pymongo import MongoClient

client = MongoClient()
db = client.gradebook
teachers = db.teachers

# TODO implement validation in validation.py
def insert(email, password, name, school):
    # TODO hash & salt
    # TODO validation for each field
    # TODO email confirmation
    if (not exists(email)):
        new_user = {
            'email' : email,
            'password' : password,
            'name' : name,
            'school' : school,
            'classes' : []
        }
        teachers.insert(new_user)
        return (True, "Registration successful. Enjoy!")
    else:
        return (False, "Registration error: A user with that email already\
                exists.")

def validate_registration(email, password):
    if (len(email) < 1):
        return (False, "Registration error: Your email must be at least 1\
                character long")
    if (len(password) < 6):
        return (False, "Registration error: Your password must be at least 6\
                characters long")
    return (True, "Registration successful. Enjoy!")

def exists(email):
    return teachers.find({'email' : email}).count() > 0

def remove(email):
    teachers.remove({'email' : email}, multi=False)

def validate_login(email, password):
    return teachers.find({'email' : email, 'password' : password}).count() == 1

def get(email):
    return teachers.find({'email': email})

def update(email, new_email=None, name=None, school=None, password=None,
           classes=None):
    if(exists(email)):
        updateDict = {}
        if new_email != None: updateDict['email'] = new_email
        if name != None: updateDict['name'] = name
        if school != None: updateDict['school'] = school
        if password != None: updateDict['password'] = password
        if classes != None: updateDict['classes'] = classes
        teachers.update(
            {'email': email},
                {'$set': updateDict}
        )
        return "Successfully updated info."
    else:
        return "Update info error: User doesn't exist!"

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

