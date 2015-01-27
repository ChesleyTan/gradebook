from pymongo import MongoClient
from validation import *
import time
from datetime import date

client = MongoClient()
db = client.gradebook
assignments = db.assignments

#aType can be like test or regular or review
#dueDate is seconds from the epoch
#i store it as different so its easier to display when requested as opposed to converting it again
def insert(courseId, name, description, dueDate, aType):
    response_tuple = isValidAssignment(name)
    if not response_tuple[0]:
        return response_tuple
    response_tuple = isValidAssignmentDescription(description)
    if not response_tuple[0]:
        return response_tuple
    response_tuple = isValidDueDate(dueDate)
    if not response_tuple[0]:
        return response_tuple
    response_tuple = isValidAssignmentType(aType)
    if not response_tuple[0]:
        return response_tuple
    if not exists(courseId, name):
        if len(str(dueDate.month)) == 1:
            d = '0'+str(dueDate.month)+'/'
        else:
            d = str(dueDate.month)+'/'
        if len(str(dueDate.day)) == 1:
            d = d+'0'+str(dueDate.day)+'/'
        else:
            d = d+str(dueDate.day)+'/'
        d = d+str(dueDate.year)
        
        new_assignment = {
            'courseId' : courseId,
            'name' : name,
            'description' : description,
            'dueDate' : d, 
            'aType' : aType
        }
        assignments.insert(new_assignment)
        return (True, "Successfully added new assignment.")
    else:
        return (False, "Error: Assignment already exists")

def exists(courseId, name):
    return assignments.find({
                                'courseId' : courseId,
                                'name' : name
                            }).count() > 0

def remove(courseId, name):
    assignments.remove({
                            'courseId' : courseId,
                            'name' : name,
                       }, multi=False)

def removeAll(courseId):
    assignments.remove({
                           'courseId' : courseId
                       })

def get(courseId):
    return assignments.find({'courseId' : courseId})
            
def update(courseId, name, new_name=None, new_description=None, new_dueDate=None, new_aType=None):
    if new_name:
        response_tuple = isValidAssignment(new_name)
        if not response_tuple[0]:
            return response_tuple
    if new_description:
        response_tuple = isValidAssignmentDescription(new_description)
        if not response_tuple[0]:
            return response_tuple
    if new_dueDate:
        response_tuple = isValidDueDate(new_dueDate)
        if not response_tuple[0]:
            return response_tuple
    if new_aType:
        response_tuple = isValidAssignmentType(new_aType)
        if not response_tuple[0]:
            return response_tuple
    if(exists(courseId, name)):
        if len(str(new_dueDate.month)) == 1:
            d = '0'+str(new_dueDate.month)+'/'
        else:
            d = str(new_dueDate.month)+'/'
        if len(str(new_dueDate.day)) == 1:
            d = d+'0'+str(new_dueDate.day)+'/'
        else:
            d = d+str(new_dueDate.day)+'/'
        d = d+str(new_dueDate.year)

        updateDict = {}
        updateDict['name'] = new_name
        updateDict['description'] = new_description
        updateDict['dueDate'] = d
        updateDict['aType'] = new_aType
        assignments.update(
            {
                'courseId' : courseId,
                'name' : name,
            },
            {
                '$set' : updateDict
            }
        )
        return (True, "Successfully updated assignment info.")
    else:
        return (False, "Error: Assignment doesn't exist!")

def dump():
    for c in assignments.find():
        print c

def drop():
    assignments.remove()

########## TESTING ##########
if __name__ == "__main__":
    drop()
    response_tuple = insert(1234567890, "Homework #1",
                            "Support the developers!", 1234567890123)
    if not response_tuple[0]:
        print response_tuple[1]
    dump()
    response_tuple = update(1234567890, "Homework #1",
                            "Support the developers!", 1234567890123,
                            new_courseId=1337, new_name="Homework #1337",
                            new_description="0x1337B33F",
                            new_dueDate=129343393939)
    if not response_tuple[0]:
        print response_tuple[1]
    dump()

# Given a Unix epoch time d,
# converts to date timestamp.
# Modify the string given as an argument to 
# strftime() in order to change the format
# (Refer to the Python library for more info)
def convert_to_date(d):
    return datetime.datetime.fromtimestamp(d).strftime('%Y-%m-%d %H:%M:%S')
