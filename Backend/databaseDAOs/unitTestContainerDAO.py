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

    def tearDown(self):
        """
        Delete the temporary database
        """
        dao = ContainerDAO()
        c = Container("101010") # c is container object 
        #r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None,None) # r is relationship object
        dao.deleteContainer(c)
        #dao.deleteRelationship(r)
    
    # TEST CREATE CONTAINER
    def testInsertContainerSmoke(self):
        c = Container("101010")
        dao = ContainerDAO()
        return dao.insertContainer(c)
    
    def testInsertContainer(self):
        """
        Test that we can add a container that doesn't exist in the database
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)
        """
        Check to see that the add went through.
        """
        qrcode = "101010"
        dao = ContainerDAO()
        rc, selectContainer = dao.selectContainer(qrcode)
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
        dao = ContainerDAO()
        
        rc, selectContainer = dao.selectContainer(qrcode)
        self.assertTrue(rc)
        self.assertEqual(qrcode,selectContainer.qrcode)
    
    def testSelectContainerDoesntExist(self):
        """
        Test that we can't select a container that doesnt exist in the database already
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)

        qrcode = "101011"
        dao = ContainerDAO()
        
        rc, selectContainer = dao.selectContainer(qrcode)
        self.assertFalse(rc)


    
    # TEST UPDATE CONTAINER
    #def testUpdateContainer(self,c): #idk if backend will need this one

    # TEST DELETE CONTAINER
    def testDeleteContainer(self):
        """
        Test that we can delete a container from the database
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)

        c = Container("101010")
        dao = ContainerDAO()
        
        rc, deleteContainer = dao.deleteContainer(c)
        self.assertTrue(rc)

        """
        Verify that the container has actually been deleted.
        """
        rc, selectContainer = dao.selectContainer("101010")
        self.assertFalse(rc)
    
    def TestDeleteContainerDoesNotExist(self):
        """
        Test that we can't delete a container that doesn't exist.
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)

        c = Container("101010")
        dao = ContainerDAO()

        rc, deleteContainer = dao.deleteContainer(c)
        self.assertTrue(rc)
        """
        QR Code already deleted.
        """
        rc, deleteContainer = dao.deleteContainer(c)
        self.assertFalse(rc)

        c = Container("101010")
        """
        QR code never in database.
        """
        rc, deleteContainer = dao.deleteContainer(c)
        self.assertFalse(rc)

        c = None
        """
        Container is NULL
        """
        rc, deleteContainer = dao.deleteContainer(c)
        self.assertFalse(rc) 

#____________________________________________________________________________________________________________________#

# the hascontainer relationship tests have moved to unitTestRelationshipDAO.py for now

if __name__ == '__main__':
    unittest.main()