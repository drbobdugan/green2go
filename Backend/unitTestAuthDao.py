import unittest
from authDao import AuthDao
class unitTestAuthDao(unittest.TestCase):
    """
    Test the authDao class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestAuthDao.py

    """
    def setUp(self):
        """
        Setup a temporary database
        """

    def tearDown(self):
        """
        Delete the temporary database
        """
        dao = AuthDao()
        auth={"email": "test42@students.stonehill.edu"}
        dao.deleteAuth(auth)
        del dao
    
    def addTest42Auth(self):
        auth={"email" : "test42@students.stonehill.edu",
            "auth_token" : "Ggpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL",
            "refresh_token" : "l9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9"}
        dao = AuthDao()
        return dao.addAuth(auth)
    
    def testRegularAddAuth(self):
        """
        Test that we can add an auth that doesn't exist in the database
        """
        rc, msg = self.addTest42Auth()
        self.assertTrue(rc)

    def testAddAuthTwice(self):
        """
        Test that we can't add an auth twice
        First add should work correctly
        """
        rc, msg = self.addTest42Auth()
        self.assertTrue(rc)

        """
        Second add should fail
        """
        rc, msg = self.addTest42Auth()
        self.assertFalse(rc)
        self.assertEqual(msg,"Duplicate Entry")
    
    def testRegularSelectAuth(self):
        """
        Test that we can select an auth that exists in the database already
        """
        rc, msg = self.addTest42Auth()
        self.assertTrue(rc)

        auth={"email": "test42@students.stonehill.edu"}
        dao = AuthDao()
        rc, getAuth = dao.getAuth(auth)

        self.assertTrue(rc)
        self.assertEqual(auth["email"],getAuth["email"])
    
    def testSelectAuthDoesntExist(self):
        """
        Test that we can't select an auth that doesn't exist in the database already
        """
        rc, msg = self.addTest42Auth()
        self.assertTrue(rc)

        auth={"email": "test43@students.stonehill.edu"}
        dao = AuthDao()
        rc, getAuth = dao.getAuth(auth)

        self.assertFalse(rc)

    def testUpdateAuth(self):
        """
        Test that we can update an auth that exists in the database already
        """
        rc, msg = self.addTest42Auth()
        self.assertTrue(rc)

        auth={"email" : "test42@students.stonehill.edu",
            "token" : "Ggpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL",
            "refresh_token" : "l9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9"}
        dao = AuthDao()
        rc, updateAuth = dao.updateAuth(auth)

        self.assertTrue(rc)

    def testDeleteAuth(self):
        """
        Test that we can delete an auth that exists in the database already
        """
        rc, msg = self.addTest42Auth()
        self.assertTrue(rc)

        auth={"email" : "test42@students.stonehill.edu",
            "auth_token" : "Ggpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL",
            "refresh_token" : "l9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9"}
        dao = AuthDao()
        rc, deleteAuth = dao.deleteAuth(auth)

        self.assertTrue(rc)

if __name__ == '__main__':
    unittest.main()