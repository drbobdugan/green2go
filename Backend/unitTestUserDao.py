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
        del dao
    
    def addTest42User(self):
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
        return dao.addUser(user)
    
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
    
    def testRegularSelectUser(self):
        """
        Test that we can select a user that exists in the database already
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        email={"email": "test42@students.stonehill.edu"}
        dao = UserDao()
        rc, getUser = dao.getUser(email)

        self.assertTrue(rc)
        self.assertEqual(email["email"],getUser["email"])
    
    def testSelectUserDoesntExist(self):
        """
        Test that we can't select a user that doesnt exist in the database already
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        email={"email": "test43@students.stonehill.edu"}
        dao = UserDao()
        rc, getUser = dao.getUser(email)

        self.assertFalse(rc)

if __name__ == '__main__':
    unittest.main()