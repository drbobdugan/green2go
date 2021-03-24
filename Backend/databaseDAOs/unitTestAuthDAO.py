import unittest
from auth import Auth
from authDAO import AuthDao

class unitTestAuthDAO(unittest.TestCase):
    """
    Test the authDAO class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestAuthDAO.py
    """
    def setUp(self):
       """
       Setup a temporary database
       """
       self.dao = AuthDao()
       self.dao.changeDatabase("temp")

    def tearDown(self):
        """
        Delete the temporary database
        """
        self.dao = AuthDao()
        auth = Auth("auth42TestUser@students.stonehill.edu","Fgpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","F9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
        self.dao.deleteAuth(auth)

    # test creating auth token
    def testInsertAuthSmoke(self):
        self.dao = AuthDao()
        auth = Auth("auth42TestUser@students.stonehill.edu","Fgpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","F9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
        return self.dao.insertAuth(auth)
    
    def testInsertAuth(self):
        """
        Test that we can add an auth token that doesn't exist in the database
        """
        rc, msg = self.testInsertAuthSmoke()
        self.assertTrue(rc)

    def testInsertAuthTwice(self):
        """
        Test that we can't add an auth token twice
        First add should work correctly
        """
        rc, msg = self.testInsertAuthSmoke()
        self.assertTrue(rc)

        """
        Second add should fail
        """
        rc, msg = self.testInsertAuthSmoke()
        self.assertFalse(rc)
        self.assertEqual(msg,"Duplicate Entry")

    def testSelectByEmail(self):
        """
        Test that we can select a location that exists in the database already
        """
        rc, msg = self.testInsertAuthSmoke()
        self.assertTrue(rc)

        email = "auth42TestUser@students.stonehill.edu"
        self.dao = AuthDao()
        rc, selectByEmail = self.dao.selectByEmail(email)

        self.assertTrue(rc)
        self.assertEqual(email,selectByEmail.user)
    
    def testselectByEmailDoesntExist(self):
        """
        Test that we can't select a location that doesnt exist in the database already
        """
        rc, msg = self.testInsertAuthSmoke()
        self.assertTrue(rc)

        email = "auth43TestUser@students.stonehill.edu"
        self.dao = AuthDao()

        rc, selectByEmail = self.dao.selectByEmail(email)
        self.assertFalse(rc)

        rc, selectByEmail = self.dao.selectByEmail(None)
        self.assertFalse(rc)

    def testUpdateAuth(self):
        """
        Test that we can update an Auth.
        """
        rc, msg = self.testInsertAuthSmoke()
        self.assertTrue(rc)

        newAuth = Auth("auth42TestUser@students.stonehill.edu","Fcpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","F9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
        self.dao = AuthDao()

        rc = self.dao.updateAuth(newAuth)
        self.assertTrue(rc)

        rc, updat = self.dao.selectByEmail(newAuth.user)
        self.assertTrue(rc)

        self.assertEqual(newAuth.auth_token, updat.auth_token)

    def testUpdateAuthDoesntExist(self):
        """
        Test that we can't update an Auth that doesn't exost.
        """
        rc, msg = self.testInsertAuthSmoke()
        self.assertTrue(rc)

        newAuth = Auth("auth43TestUser@students.stonehill.edu","Fcpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","F9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
        self.dao = AuthDao()

        rc, updat = self.dao.selectByEmail(newAuth.user)
        self.assertFalse(rc)

        rc, updat = self.dao.selectByEmail(None)
        self.assertFalse(rc)


    def testDeleteAuth(self):
        """
        Test that we can delete an auth from the database
        """
        rc, msg = self.testInsertAuthSmoke()
        self.assertTrue(rc)


        auth = Auth("auth42TestUser@students.stonehill.edu","Fgpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","F9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
        self.dao = AuthDao()
        
        rc, deleteAuth = self.dao.deleteAuth(auth)
        self.assertTrue(rc)

        rc, selectByEmail = self.dao.selectByEmail(auth.user)
        self.assertFalse(rc)

    def testDeleteAuthDoesntExist(self):
        """
        Test that we can't delete an auth that doesn't exist
        """
        rc, msg = self.testInsertAuthSmoke()
        self.assertTrue(rc)


        auth = Auth("auth42TestUser@students.stonehill.edu","Fgpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","F9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
        self.dao = AuthDao()
        
        rc, deleteAuth = self.dao.deleteAuth(auth)
        self.assertTrue(rc)

        rc, deleteAuth = self.dao.deleteAuth(auth)
        self.assertFalse(rc)

        auth = Auth("auth43TestUser@students.stonehill.edu","Fgpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","F9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")

        rc, deleteAuth = self.dao.deleteAuth(auth)
        self.assertFalse(rc)

        rc, deleteAuth = self.dao.deleteAuth(None)
        self.assertFalse(rc)

if __name__ == '__main__':
    unittest.main()
    