from pymongo import MongoClient
from bson.objectid import ObjectId
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
            'students' : [],
            'courseRequests' : []
        }
        courses.insert(new_courses)
        return (True, "Successfully added new course")
    else:
        return (False, "Error: Course already exists")

def exists(teacherId, name, courseId=None):
    if courseId:
        try:
            return courses.find({'_id' : ObjectId(courseId)}).count() > 0
        except:
            return False
    else:
        return courses.find({
                                'teacherId' : teacherId,
                                'name' : name
                            }).count() > 0

def remove(teacherId, name):
    courses.remove({
                        'teacherId' : teacherId,
                        'name' : name
                    }, multi=False)

def removeAll(teacherId):
    courses.remove({
                        'teacherId' : teacherId
                    })

def get(courseId):
    try:
        id = ObjectId(courseId)
        return courses.find({'_id': id})
    except:
        return None

def getByTeacher(teacherId, name=None):
    if name:
        return courses.find({'teacherId': teacherId, 'name': name})
    else:
        return courses.find({'teacherId': teacherId})

def update(teacherId, name, courseId=None, new_teacherId=None, new_name=None,
           new_description=None, new_students=None,
           course_requests=None):
    if new_name:
        response_tuple = isValidCourse(new_name)
        if not response_tuple[0]:
            return response_tuple
    if new_description:
        response_tuple = isValidCourseDescription(new_description)
        if not response_tuple[0]:
            return response_tuple
    if(exists(teacherId, name, courseId)):
        updateDict = {}
        if new_teacherId != None: updateDict['teacherId'] = new_teacherId
        if new_name != None: updateDict['name'] = new_name
        if new_description != None: updateDict['description'] = new_description
        if new_students != None: updateDict['students'] = new_students
        if course_requests != None: updateDict['courseRequests'] = course_requests
        if courseId:
            try:
                courses.update(
                    {
                        '_id': ObjectId(courseId)
                    },
                        {'$set': updateDict}
                )
            except:
                return (False, "Error: Invalid course id")
        else:
            courses.update(
                {
                    'teacherId': teacherId,
                    'name' : name
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

def getCourseRequests(courseId):
    course_cursor = None
    try:
        course_cursor = courses.find({'_id' : ObjectId(courseId)},
            { 'courseRequests' : 1})
    except:
        return None
    if course_cursor.count() == 1:
        course_requests = course_cursor[0]
        if course_requests.has_key('courseRequests'):
            return course_requests['courseRequests']
        else:
            return []
    else:
        return None

def addCourseRequest(courseId, studentId):
    courseRequests = getCourseRequests(courseId)
    if courseRequests != None and studentId not in courseRequests:
        courseRequests.append(studentId)
        update('', '', courseId, course_requests=courseRequests)

def removeCourseRequest(courseId, studentId):
    courseRequests = getCourseRequests(courseId)
    if courseRequests != None and studentId in courseRequests:
        courseRequests.remove(studentId)
        update('', '', courseId=courseId, course_requests=courseRequests)

def getStudents(courseId):
    course_cursor = None
    try:
        course_cursor = courses.find({'_id' : ObjectId(courseId)},
            { 'students' : 1})
    except:
        return None
    if course_cursor.count() == 1:
        course_cursor = course_cursor[0]
        if course_cursor.has_key('students'):
            return course_cursor['students']
        else:
            return []
    else:
        return None

def addStudentToCourseAndRemoveRequest(courseId, studentId):
    students = getStudents(courseId=courseId)
    if students != None and studentId not in students:
        students.append(studentId)
        update('', '', courseId, new_students=students)
    removeCourseRequest(courseId, studentId)

########## TESTING ##########
#if __name__ == "__main__":
#    drop()
#    response_tuple = insert(1234567890, 
#                            "AP Advanced Polyvariate Calculus Accelerated",
#                            "Applications of probabilistic statistical "
#                            "analysis with calculus")
#    if not response_tuple[0]:
#        print response_tuple[1]
#    dump()
#    response_tuple = update(1234567890,
#                "AP Advanced Polyvariate Calculus Accelerated",
#                "Applications of probabilistic statistical analysis with "
#                "calculus",
#                new_teacherId=1337, new_name="Hacking 101",
#                new_description="0x1337B33F",
#                new_students=["Elvin", "Junhao", "Eric", "Elmo"])
#    if not response_tuple[0]:
#        print response_tuple[1]
#    dump()
#
