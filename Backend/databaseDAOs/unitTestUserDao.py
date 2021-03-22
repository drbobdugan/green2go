import unittest
from userDAO import UserDao
from user import User
class unitTestUserDao(unittest.TestCase):
    """
    Test the userDao class methods using the unit test framework.  
    To run these tests:
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
        user = dao.getUser("test42@students.stonehill.edu")
        dao.deleteUser(user[1])
        del dao
    
    def addTest42User(self):
        user = User(
                "test42@students.stonehill.edu",
                "password",
                "Test",
                "User",
                "Example",
                "7817817811",
                "RegularUser",
                "2021",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0")
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

        email="test42@students.stonehill.edu"
        dao = UserDao()
        rc, getUser = dao.getUser(email)

        self.assertTrue(rc)
        self.assertEqual(email,getUser.email)
    
    def testSelectUserDoesntExist(self):
        """
        Test that we can't select a user that doesnt exist in the database already
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        email="test43@students.stonehill.edu"
        dao = UserDao()
        rc, getUser = dao.getUser(email)

        self.assertFalse(rc)

if __name__ == '__main__':
    unittest.main()