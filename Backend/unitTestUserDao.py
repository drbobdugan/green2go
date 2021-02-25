import unittest
from userDao import UserDao
class unitTestUserDao(unittest.TestCase):
    """
    Test the userDao class methods using the unit test framework.  To run these tests:

         python3 -m unittest unitTestUserDao.py

    """
    def setUp(self):
        """
        Setup a temporary database
        """

    def tearDown(self):
        """
        Delete the temporary database
        """
        dao = UserDao()
        emailDict={"email": "test42@students.stonehill.edu"}
        dao.deleteUser(emailDict)
    
    def testRegularAddUser(self):
        """
        Test that we can add a user that doesn't exist in the database
        """
        user={
                "email": "test42@students.stonehill.edu",
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
        dao = UserDao()
        dao.addUser(user)

        email={"email": "test42@students.stonehill.edu"}
        rc, getUser = dao.getUser(email)
        print("user:", user)
        print("getuser:", getUser)
        ignore_keys = ["authTime","lastLogIn"]
        filteredUser  = {k: v for k,v in user.items() if k not in ignore_keys} 
        filteredGetUser = {k: v for k,v in getUser.items() if k not in ignore_keys} 
        self.assertEqual(filteredUser,filteredGetUser)

    def testAddUserTwice(self):
        """
        Test that we can add a user that doesn't exist in the database
        """
        user={
                "email": "test42@students.stonehill.edu",
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
        dao = UserDao()
        dao.addUser(user)
        rc, msg = dao.addUser(user)

        self.assertEqual(rc,False)
        self.assertEqual(msg,"Duplicate Entry")

if __name__ == '__main__':
    unittest.main()