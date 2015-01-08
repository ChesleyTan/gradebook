from pymongo import MongoClient

client = MongoClient()
db = client.gradebook
assignments = db.assignments

def insert(courseId, name, description, dueDate):
    # TODO validation for each field
    new_assignment = {
        'courseId' : courseId,
        'name' : name,
        'description' : description,
        'dueDate' : dueDate
    }
    assignments.insert(new_assignment)
    return (True, "Successfully added new assignment.")

def exists(courseId, name, description, dueDate):
    return assignments.find({
                                'courseId' : courseId,
                                'name' : name,
                                'description' : description,
                                'dueDate' : dueDate
                            }).count() > 0

def remove(courseId, name, description, dueDate):
    assignments.remove({
                            'courseId' : courseId,
                            'name' : name,
                            'description' : description,
                            'dueDate' : dueDate
                       }, multi=False)

def removeAll(courseId):
    assignments.remove({
                           'courseId' : courseId
                       })

def get(courseId):
    return assignments.find({'courseId': courseId})

def update(courseId, name, description, dueDate, new_courseId=None,
           new_name=None, new_description=None, new_dueDate=None):
    if(exists(courseId, name, description, dueDate)):
        updateDict = {}
        if new_courseId != None: updateDict['courseId'] = new_courseId
        if new_name != None: updateDict['name'] = new_name
        if new_description != None: updateDict['description'] = new_description
        if new_dueDate != None: updateDict['dueDate'] = new_dueDate
        assignments.update(
            {
                'courseId': courseId,
                'name' : name,
                'description' : description,
                'dueDate' : dueDate
            },
                {'$set': updateDict}
        )
        return "Successfully updated assignment info."
    else:
        return "Update info error: Assignment doesn't exist!"

def dump():
    for c in assignments.find():
        print c

def drop():
    assignments.remove()

########## TESTING ##########
if __name__ == "__main__":
    drop()
    response_tuple = insert(1234567890, "Homework #1",
                            "Support the developers!", 1234567890)
    if not response_tuple[0]:
        print response_tuple[1]
    dump()
    update(1234567890, "Homework #1", "Support the developers!", 1234567890,
           new_courseId=1337, new_name="Homework #1337",
           new_description="0x1337B33F", new_dueDate=9393939)
    dump()

