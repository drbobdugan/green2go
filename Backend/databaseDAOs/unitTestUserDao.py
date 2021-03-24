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
        self.dao = UserDao()
        self.dao.changeDatabase("temp")


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
                "2021",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0",
                "exampletoken")
        return self.dao.insertUser(user)
    
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
                "2021",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0",
                "exampletoken")

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
                "2021",
                "1111111",
                "2021-01-01 01:01:01",
                "2021-01-01 01:01:01",
                "0",
                "exampletoken")

        rc, msg = self.dao.updateUser(user)
        self.assertFalse(rc)

        rc, msg = self.dao.updateUser(None)
        self.assertFalse(rc)         


    def testDeleteUser(self):

        """
        Test that we can delete a user from the database.
        """
        rc, msg = self.addTest42User()
        self.assertTrue(rc)

        email="test42@students.stonehill.edu"
        rc, getUser = self.dao.selectUser(email)
        self.assertTrue(rc)
        """
        Delete the user
        """
        rc, deleteUser = self.dao.deleteUser(getUser)
        self.assertTrue(rc)

        """
        Check if container is actually deleted
        """
        rc, getUser = self.dao.selectUser(email)
        self.assertFalse(rc)

if __name__ == '__main__':
    unittest.main()