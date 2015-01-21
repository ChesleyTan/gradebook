from pymongo import MongoClient
from validation import *

client = MongoClient()
db = client.gradebook
courses = db.courses

def insert(teacherId, name, description):
    response_tuple = isValidCourse(name)
    if not response_tuple[0]:
        return response_tuple
    response_tuple = isValidCourseDescription(description)
    if not response_tuple[0]:
        return response_tuple
    if not exists(teacherId, name):
        new_courses = {
            'teacherId' : teacherId,
            'name' : name,
            'description' : description,
            'students' : []
        }
        courses.insert(new_courses)
        return (True, "Successfully added new course")
    else:
        return (False, "Error: Course already exists")

def exists(teacherId, name):
    return courses.find({
                            'teacherId' : teacherId,
                            'name' : name
                        }).count() > 0

def remove(teacherId, name, description):
    courses.remove({
                        'teacherId' : teacherId,
                        'name' : name,
                        'description' : description
                    }, multi=False)

def removeAll(teacherId):
    courses.remove({
                        'teacherId' : teacherId
                    })

def get(teacherId):
    return courses.find({'teacherId': teacherId})

def update(teacherId, name, description, new_teacherId=None, new_name=None,
           new_description=None, new_students=None):
    if new_name:
        response_tuple = isValidCourse(new_name)
        if not response_tuple[0]:
            return response_tuple
    if new_description:
        response_tuple = isValidCourseDescription(new_description)
        if not response_tuple[0]:
            return response_tuple
    if(exists(teacherId, name)):
        updateDict = {}
        if new_teacherId != None: updateDict['teacherId'] = new_teacherId
        if new_name != None: updateDict['name'] = new_name
        if new_description != None: updateDict['description'] = new_description
        if new_students != None: updateDict['students'] = new_students
        courses.update(
            {
                'teacherId': teacherId,
                'name' : name,
                'description' : description
            },
                {'$set': updateDict}
        )
        return (True, "Successfully updated course info.")
    else:
        return (False, "Error: Course doesn't exist!")

def dump():
    for c in courses.find():
        print c

def drop():
    courses.remove()

########## TESTING ##########
if __name__ == "__main__":
    drop()
    response_tuple = insert(1234567890, 
                            "AP Advanced Polyvariate Calculus Accelerated",
                            "Applications of probabilistic statistical "
                            "analysis with calculus")
    if not response_tuple[0]:
        print response_tuple[1]
    dump()
    response_tuple = update(1234567890,
                "AP Advanced Polyvariate Calculus Accelerated",
                "Applications of probabilistic statistical analysis with "
                "calculus",
                new_teacherId=1337, new_name="Hacking 101",
                new_description="0x1337B33F",
                new_students=["Elvin", "Junhao", "Eric", "Elmo"])
    if not response_tuple[0]:
        print response_tuple[1]
    dump()

