import unittest
from userDAO import UserDAO
from user import User
class unitTestUserDAO(unittest.TestCase):
    """
    Test the userDAO class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestUserDao.py
    """

    def setUp(self):
        """
        Setup a temporary database
        """
        self.dao = UserDAO()

    def tearDown(self):
        """
        Delete the temporary database
        """
        user = self.dao.selectUser("test42@students.stonehill.edu")
        self.dao.deleteUser(user[1])
        del self.dao
    
    def addTest42User(self):
        user = User(
                "test42@students.stonehill.edu",
                "password",
                "Test",
                "User",
                "Example",
                "7817817811",
                "RegularUser",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0",
                "exampletoken",
                5,
                "2021-01-01 02:02:02")
        return self.dao.insertUser(user)
    
    def testUserSizeLimits(self):
        lim45 = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        user = User(
                lim45,
                "password",
                "Test",
                "User",
                "Example",
                "7817817811",
                "RegularUser",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0",
                "exampletoken",
                5,
                "2021-01-01 02:02:02")
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("email is too long" in msg)

        user.email = "test42@students.stonehill.edu"
        password = user.password
        user.password = lim45 + lim45 + lim45
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("password is too long" in msg)

        user.password = password
        firstName = user.firstName
        user.firstName = lim45
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("firstName is too long" in msg)

        user.firstName = firstName
        lastName = user.lastName
        user.lastName = lim45
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("lastName is too long" in msg)

        user.lastName = lastName
        middleName = user.middleName
        user.middleName = lim45
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("middleName is too long" in msg)

        user.middleName = middleName
        phoneNum = user.phoneNum
        user.phoneNum = "xxxxxxxxxxxxxxxx"
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("phoneNum is too long" in msg)

        user.phoneNum = phoneNum
        role = user.role
        user.role = lim45
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("role is too long" in msg)

        authCode = user.authCode
        user.authCode = lim45
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("authCode is too long" in msg)

        user.authCode = authCode
        authorized = user.authorized
        user.authorized = "xx"
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("authorized is too long" in msg)

        user.authorized = authorized
        user.beams_token = lim45 + lim45 + lim45 + lim45 + lim45 + lim45 + lim45 + lim45 + lim45 + lim45
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("beams_token is too long" in msg)

        points = user.points
        user.points = 999999999999
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        self.assertTrue("points is too long" in msg)

    def testRegularAddUser(self):
        """
        Test that we can add a user that doesn't exist in the database
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

    def testAddUserTwice(self):
        """
        Test that we can't add a user twice
        First add should work correctly
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        """
        Second add should fail
        """
        rc, msg = self.addTest42User()
        self.assertFalse(rc)
        self.assertEqual(msg,"Duplicate Entry")
    
    def addUserNoneType(self):
        user = User(
                None,
                "password",
                "Test",
                "User",
                "Example",
                "7817817811",
                "RegularUser",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0",
                "exampletoken",
                5,
                "2021-01-01 02:02:02")
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.email = "test42@students.stonehill.edu"

        user.password = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.password = "password"

        user.firstName = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.firstName = "Test"

        user.middleName = None
        rc, msg = self.dao.insertUser(user)
        self.assertTrue(rc)
        user.middleName = "Example"
        rc, deleteUser = self.dao.deleteUser(user.email)
        self.assertTrue(rc)

        user.lastName = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.lastName = "User"

        user.phoneNum = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.phoneNum = "7817817811"

        user.role = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.role = "RegularUser"

        user.authCode = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.authCode = "123456"

        user.authTime = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.authTime = "123456"

        user.lastLogIn = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.lastLogIn = "2021-01-01 01:01:01"

        user.authorized = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.authorized = "0"

        user.beams_token = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.beams_token = "exampletoken"

        user.points = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.points = 5

        user.reward_date = None
        rc, msg = self.dao.insertUser(user)
        self.assertFalse(rc)
        user.reward_date = "2021-01-01 02:02:02"

    def testRegularSelectUser(self):
        """
        Test that we can select a user that exists in the database already
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        email="test42@students.stonehill.edu"
        rc, getUser = self.dao.selectUser(email)

        self.assertTrue(rc)
        self.assertEqual(email,getUser.email)
    
    def testSelectUserDoesntExist(self):
        """
        Test that we can't select a user that doesnt exist in the database already
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        email="test43@students.stonehill.edu"
        rc, getUser = self.dao.selectUser(email)

        self.assertFalse(rc)

    def testUpdateUser(self):
        """
        Test that the user can be updated.
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        user = User(
                "test42@students.stonehill.edu",
                "password",
                "Test",
                "Lazer",
                "Example",
                "1111111111",
                "RegularUser",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0",
                "exampletoken",
                5,
                "2021-01-01 02:02:02")

        rc, msg = self.dao.updateUser(user)
        self.assertTrue(rc)

        rc, msg = self.dao.selectUser(user.email)
        self.assertTrue(rc)
        self.assertEqual(user.phoneNum, msg.phoneNum)
        self.assertEqual(user.middleName, msg.middleName)

    def testUpdateUserDoesntExist(self):
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        user = User(
                "test43@students.stonehill.edu",
                "password",
                "Test",
                "Lazer",
                "Example",
                "1111111111",
                "RegularUser",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0",
                "exampletoken",
                5,
                "2021-01-01 02:02:02")

        #rc, msg = self.dao.updateUser(user)
        #self.assertFalse(rc)

        #rc, msg = self.dao.updateUser(None)
        #self.assertFalse(rc)         

    def testDeleteUser(self):
        """
        Test that we can delete a user from the database.
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)
        
        #get user
        email="test42@students.stonehill.edu"
        rc, getUser = self.dao.selectUser(email)
        self.assertTrue(rc)

        #delete user
        rc, deleteUser = self.dao.deleteUser(getUser)
        self.assertTrue(rc)

        #check if user is actually deleted
        rc, getUser = self.dao.selectUser(email)
        self.assertFalse(rc)

    def testDeleteUserDoesntExist(self):
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        email="test42@students.stonehill.edu"

        rc, getUser = self.dao.selectUser(email)
        self.assertTrue(rc)

        rc, deleteUser = self.dao.deleteUser(getUser)
        self.assertTrue(rc)

        """
        Can't delete a user that's already been deleted
        """
        rc, deleteUser = self.dao.deleteUser(getUser)
        self.assertFalse(rc)

        """
        Can't delete a user that was never there to begin with
        """
        user = User(
                "test43@students.stonehill.edu",
                "password",
                "Test",
                "Lazer",
                "Example",
                "1111111111",
                "RegularUser",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0",
                "exampletoken",
                5,
                "2021-01-01 02:02:02")

        rc, msg = self.dao.deleteUser(user)
        self.assertFalse(rc)

        """
        Can't delete a NoneType user
        """
        rc, msg = self.dao.deleteUser(None)
        self.assertFalse(rc)

if __name__ == '__main__':
    unittest.main()