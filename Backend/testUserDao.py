from userDao import UserDao
dao = UserDao()
def main():
    testAddUser()
    testGetUser()
    testDeleteUser()

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
    #dao.addUser(val)
    email = "test1@students.stonehill.edu"
    val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    #dao.addUser(val)
    email = "test2@students.stonehill.edu"
    val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    #dao.addUser(val)
    email = "test3@students.stonehill.edu"
    val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    dao.addUser(val)
    
def testGetUser():
    email = "test@students.stonehill.edu"
    dao.getUser(email)
    email = "test1@students.stonehill.edu"
    dao.getUser(email)
    email = "test2@students.stonehill.edu"
    dao.getUser(email)
    email = "test3@students.stonehill.edu"
    dao.getUser(email)
def testDeleteUser():
    email = "test@students.stonehill.edu"
    dao.deleteUser(email)
    email = "test1@students.stonehill.edu"
    dao.deleteUser(email)
    email = "test2@students.stonehill.edu"
    dao.deleteUser(email)
    email = "test3@students.stonehill.edu"
    dao.deleteUser(email)

    


main()