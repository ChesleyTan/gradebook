from pymongo import MongoClient

client = MongoClient()
db = client.gradebook
courses = db.courses

def insert(teacherId, name, description):
    # TODO validation for each field
    new_courses = {
        'teacherId' : teacherId,
        'name' : name,
        'description' : description,
        'students' : []
    }
    courses.insert(new_courses)
    return (True, "Successfully added new course.")

def exists(teacherId, name, description):
    return courses.find({
                                'teacherId' : teacherId,
                                'name' : name,
                                'description' : description
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
    if(exists(teacherId, name, description)):
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
        return "Successfully updated course info."
    else:
        return "Update info error: Course doesn't exist!"

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
    print update(1234567890, "AP Advanced Polyvariate Calculus Accelerated",
                 "Applications of probabilistic statistical analysis with "
                 "calculus",
                 new_teacherId=1337, new_name="Hacking 101",
                 new_description="0x1337B33F",
                 new_students=["Elvin", "Junhao", "Eric", "Elmo"])
    dump()

