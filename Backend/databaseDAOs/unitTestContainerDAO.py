import unittest
from containerDAO import ContainerDAO
from container import Container
from relationship import Relationship

class unitTestContainerDAO(unittest.TestCase):
    """
    Test the containerDAO class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestContainerDAO.py
    """
    def setUp(self):
       """
       Setup a temporary database
       """
       self.dao = ContainerDAO()
       self.dao.changeDatabase("temp")

    def tearDown(self):
        """
        Delete the temporary database
        """
        c = Container("101010") # c is container object 
        self.dao.deleteContainer(c)
        del self.dao
    
    # TEST CREATE CONTAINER
    def testInsertContainerSmoke(self):
        c = Container("101010")
        return self.dao.insertContainer(c)
    
    def testInsertContainer(self):
        """
        Test that we can add a container that doesn't exist in the database
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)
        """
        Check to see that the add went through
        """
        qrcode = "101010"
        rc, selectContainer = self.dao.selectContainer(qrcode)
        self.assertTrue(rc)
        self.assertEqual(qrcode,selectContainer.qrcode)

    def testInsertContainerTwice(self):
        """
        Test that we can't add a container twice
        First add should work correctly
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)

        """
        Second add should fail
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertFalse(rc)
        self.assertEqual(msg,"Duplicate Entry")
    
    # TEST READ CONTAINER
    def testSelectContainer(self):
        """
        Test that we can select a container that exists in the database already
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)
        
        qrcode = "101010"
        rc, selectContainer = self.dao.selectContainer(qrcode)
        self.assertTrue(rc)
        self.assertEqual(qrcode,selectContainer.qrcode)
    
    def testSelectContainerDoesntExist(self):
        """
        Test that we can't select a container that doesnt exist in the database already
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)

        qrcode = "101011"
        rc, selectContainer = self.dao.selectContainer(qrcode)
        self.assertFalse(rc)

        qrcode = None
        rc, selectContainer = self.dao.selectContainer(qrcode)
        self.assertFalse(rc)
    
    # TEST UPDATE CONTAINER
    #def testUpdateContainer(self,c): #idk if we will ever need this

    # TEST DELETE CONTAINER
    def testDeleteContainer(self):
        """
        Test that we can delete a container from the database
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)

        c = Container("101010")
        rc, deleteContainer = self.dao.deleteContainer(c)
        self.assertTrue(rc)

        """
        Verify that the container has actually been deleted.
        """
        rc, selectContainer = self.dao.selectContainer("101010")
        self.assertFalse(rc)
    
    def TestDeleteContainerDoesNotExist(self):
        """
        Test that we can't delete a container that doesn't exist.
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)

        c = Container("101010")
        rc, deleteContainer = self.dao.deleteContainer(c)
        self.assertTrue(rc)
        """
        QR Code already deleted.
        """
        rc, deleteContainer = self.dao.deleteContainer(c)
        self.assertFalse(rc)

        c = Container("101010")
        """
        QR code never in database.
        """
        rc, deleteContainer = self.dao.deleteContainer(c)
        self.assertFalse(rc)

        c = None
        """
        Container is NULL
        """
        rc, deleteContainer = self.dao.deleteContainer(c)
        self.assertFalse(rc) 

if __name__ == '__main__':
    unittest.main()