import unittest
from appInfoDAO import appInfoDAO
from appInfo import appInfo

class unitTestAppInfoDAO(unittest.TestCase):
    """
    Test the containerDAO class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestAppInfoDAO.py
    """
    def setUp(self):
        self.dao = appInfoDAO()


    def tearDown(self):
        """
        Delete the temporary database
        """
        temp = appInfo(0,0,0,"test")
        self.dao.deleteAppInfo(temp)
        del self.dao
    
    # TEST CREATE CONTAINER
    def testInsertAppInfoSmoke(self):
        a = appInfo(0,0,0,"test")
        return self.dao.insertAppInfo(a)
    
    def testInsertAppInfo(self):
        """
        Test that we can add a container that doesn't exist in the database
        """
        rc, msg = self.testInsertAppInfoSmoke()
        self.assertTrue(rc)
        """
        Check to see that the add went through
        """
        temp = appInfo(0,0,0,"test")
        rc, selectAppInfo = self.dao.selectAppInfo("test")
        self.assertTrue(rc)
        self.assertEqual(temp.appInfoToList(),selectAppInfo.appInfoToList())
    
    # TEST READ CONTAINER
    def testSelectAppInfo(self):
        """
        Test that we can select a container that exists in the database already
        """
        rc, msg = self.testInsertAppInfoSmoke()
        self.assertTrue(rc)
        
        a = appInfo(0,0,0,"test")
        rc, selectAppInfo = self.dao.selectAppInfo("test")
        self.assertTrue(rc)
        self.assertEqual(a.appInfoToList(),selectAppInfo.appInfoToList())
    
    # TEST UPDATE CONTAINER
    def testUpdateAppInfo(self):
        """
        Test that we can update a container in the database
        """
        a = appInfo(0,0,0,"test")
        rc, msg = self.dao.insertAppInfo(a)
        self.assertTrue(rc)

        a.major = a.major+ 1
        rc, updateAppInfo = self.dao.updateAppInfo(a)
        self.assertTrue(rc)

        rc, temp = self.dao.selectAppInfo("test")
        self.assertTrue(rc)
        self.assertTrue(temp.major == a.major)

    # TEST DELETE CONTAINER
    def testDeleteContainer(self):
        """
        Test that we can delete a container from the database
        """
        rc, msg = self.testInsertAppInfoSmoke()
        self.assertTrue(rc)

        a = appInfo(0,0,0,"test")
        rc, deleteAppInfo= self.dao.deleteAppInfo(a)
        self.assertTrue(rc)

        """
        Verify that the container has actually been deleted.
        """
        rc, selectAppInfo= self.dao.selectAppInfo("test")
        self.assertFalse(rc)
    
   
if __name__ == '__main__':
    unittest.main()