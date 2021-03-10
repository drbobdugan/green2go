from userDao import UserDao
dao = UserDao()
def main():
    testAddUser()
    testGetUser()
    testUpdateUser()
    testDeleteUser()

#user test include creating, reading, updating, and deleting
def testAddUser():
    userDict={
                "email": "test@students.stonehill.edu",
                "password": "password",
                "firstName": "Test",
                "lastName": "User",
                "middleName":"Example",
                "phoneNum": "7817817811",
                "role": "RegularUser",
                "classYear": "2021",
                "authCode": "1111111",
                "authTime": "2021-01-01 01:01:01",
                "lastLogIn": "2021-01-01 01:01:01"}
    dao.addUser(userDict)
    userDict['email']= "test1@students.stonehill.edu"
    dao.addUser(userDict)
    userDict['email']= "test2@students.stonehill.edu"
    dao.addUser(userDict)
    userDict['email']= "test3@students.stonehill.edu"
    dao.addUser(userDict)
    
def testGetUser():
    emailDict={"email": "test@students.stonehill.edu"}
    userDict = dao.getUser(emailDict)
    print("testGetUser: test0")
    #print(testUserDict(userDict,email))
    emailDict={"email": "test1@students.stonehill.edu"}
    userDict = dao.getUser(emailDict)
    print("testGetUser: test1")
    #print(testUserDict(userDict,email))
    emailDict={"email": "test2@students.stonehill.edu"}
    userDict = dao.getUser(emailDict)
    print("testGetUser: test2")
    #print(testUserDict(userDict,email))
    emailDict={"email": "test3@students.stonehill.edu"}
    userDict = dao.getUser(emailDict)
    print("testGetUser: test3")
    #print(testUserDict(userDict,email))

def testUpdateUser():
    userDict={
                "email": "test@students.stonehill.edu",
                "password": "newPassword",
                "firstName": "newFirstName",
                "lastName": "newLastName",
                "middleName":"newMiddleName",
                "phoneNum": "newPhoneNum",
                "role": "Role",
                "classYear": None,
                "authCode": "newAuthCode",
                "authTime": None,
                "lastLogIn": None}
    dao.updateUser(userDict)

def testDeleteUser():
    emailDict={"email": "test@students.stonehill.edu"}
    dao.deleteUser(emailDict)
    emailDict={"email": "test1@students.stonehill.edu"}
    dao.deleteUser(emailDict)
    emailDict={"email": "test2@students.stonehill.edu"}
    dao.deleteUser(emailDict)
    emailDict={"email": "test3@students.stonehill.edu"}
    dao.deleteUser(emailDict)

def testUserDict(userDict,email):
    return (userDict["email"] == email and userDict["password"] == "password" 
    and userDict["firstName"] == "Test" and userDict["lastName"] == "User"
    and userDict["middleName"] == "Example" and userDict["phoneNum"] == "7817817811"
    and userDict["role"] == "reus" and userDict["classYear"] == "2021"
    and userDict["authCode"] == "111111" and userDict["authTime"] == "2021-01-01 01:01:01"
    and userDict["lastLogIn"] == "2021-01-01 01:01:01")

main()