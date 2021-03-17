import unittest
from containerDAO import containerDAO
#import object classes?

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
        r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None,None) # r is relationship object
        dao.deleteContainer(c)
        dao.deleteRelationship(r)
    
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
        
        c = Container("101010")
        dao = ContainerDAO()
        
        rc, getContainer = dao.selectContainer(c)
        self.assertTrue(rc)
        self.assertEqual(container["qrcode"],getContainer["qrcode"])
    
    def testSelectContainerDoesntExist(self):
        """
        Test that we can't select a container that doesnt exist in the database already
        """
        rc, msg = self.testInsertContainerSmoke()
        self.assertTrue(rc)

        c = Container("101010")
        dao = ContainerDAO()
        
        rc, msg = dao.deleteContainer(c)
        self.assertTrue(rc)
        
        rc, getContainer = dao.getContainer(c)
        self.assertFalse(rc)
    
    # TEST UPDATE CONTAINER
    #def testUpdateContainer(self): #idk if backend will need this one

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

#____________________________________________________________________________________________________________________#
    
    # TEST CREATE RELATIONSHIP
    def testInsertRelationshipSmoke(self):
        r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None, None)
        dao = ContainerDAO()
        return dao.addRelationship(rel)
    
    def testInsertRelationship(self):
        """
        Test that we can add a relationship that doesn't exist in the database
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

    def testInsertRelationshipTwice(self):
        """
        Test that we can add a relationship twice
        First add should work correctly
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        """
        Second add should not fail
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

    # TEST READ RELATIONSHIP
    def testSelectRelationship(self):
        """
        Test that we can select a relationship that exists in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None, None)
        dao = ContainerDAO()
        
        rc, getRelationship = dao.getRelationship(r)
        self.assertTrue(rc)
    
    def testSelectRelationshipDoesntExist(self):
        """
        Test that we can't select a relationship that doesnt exist in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None, None)
        dao = ContainerDAO()
        
        rc, msg = dao.deleteRelationship(r)
        self.assertTrue(rc)
        
        rc, getRelationship = dao.getRelationship(r)
        self.assertFalse(rc)

    # TEST UPDATE RELATIONSHIP
    def testUpdateRelationship(self):
        """
        Test that we can update a relationship that exists in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None, None)
        dao = ContainerDAO()
        
        rc, updateRelationship = dao.updateRelationship(r)
        self.assertTrue(rc)

    # TEST DELETE RELATIONSHIP
    def testDeleteRelationship(self):
        """
        Test that we can delete a relationship that exists in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None, None)
        dao = ContainerDAO()
       
       rc, deleteRelationship = dao.deleteRelationship(r)
        self.assertTrue(rc)

if __name__ == '__main__':
    unittest.main()