from userDao import UserDao
dao = UserDao()
def main():
    #testAddUser()
    testGetUser()
    #testDeleteUser()

def testAddUser():
    email = "test@students.stonehill.edu"
    password = "password"
    firstName = "Test"
    lastName = "User"
    middleName="Example"
    phoneNum = "7817817811"
    role = "reus"
    classYear = "2021"
    authCode= "111111"
    authTime= "2021-01-01 01:01:01"
    lastLogIn= "2021-01-01 01:01:01"
    val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    dao.addUser(val)
    email = "test1@students.stonehill.edu"
    val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    dao.addUser(val)
    email = "test2@students.stonehill.edu"
    val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    dao.addUser(val)
    email = "test3@students.stonehill.edu"
    val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    dao.addUser(val)
    
def testGetUser():
    email = "test@students.stonehill.edu"
    userDict = dao.getUser(email)
    print("testGetUser: test0")
    print(testUserDict(userDict,email))
    email = "test1@students.stonehill.edu"
    userDict = dao.getUser(email)
    print("testGetUser: test1")
    print(testUserDict(userDict,email))
    email = "test2@students.stonehill.edu"
    userDict = dao.getUser(email)
    print("testGetUser: test2")
    print(testUserDict(userDict,email))
    email = "test3@students.stonehill.edu"
    userDict= dao.getUser(email)
    print("testGetUser: test2")
    print(testUserDict(userDict,email))
def testDeleteUser():
    email = "test@students.stonehill.edu"
    dao.deleteUser(email)
    email = "test1@students.stonehill.edu"
    dao.deleteUser(email)
    email = "test2@students.stonehill.edu"
    dao.deleteUser(email)
    email = "test3@students.stonehill.edu"
    dao.deleteUser(email)
def testUserDict(userDict,email):
    return (userDict["email"] == email and userDict["password"] == "password" 
    and userDict["firstName"] == "Test" and userDict["lastName"] == "User"
    and userDict["middleName"] == "Example" and userDict["phoneNum"] == "7817817811"
    and userDict["role"] == "reus" and userDict["classYear"] == "2021"
    and userDict["authCode"] == "111111" and userDict["authTime"] == "2021-01-01 01:01:01"
    and userDict["lastLogIn"] == "2021-01-01 01:01:01")


    


main()