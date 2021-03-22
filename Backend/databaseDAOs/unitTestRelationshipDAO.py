import unittest
from relationshipDAO import RelationshipDAO
from relationship import Relationship

class unitTestRelationshipDAO(unittest.TestCase):
    """
    Test the relationshipDAO class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestRelationshipDAO.py
    """
    def setUp(self):
       """
       Setup a temporary database
       """

    def tearDown(self):
        """
        Delete the temporary database
        """
        dao = RelationshipDAO()
        #c = Container("101010") # c is container object 
        r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None,None) # r is relationship object
        #dao.deleteContainer(c)
        dao.deleteRelationship(r)

    # TEST CREATE RELATIONSHIP
    def testInsertRelationshipSmoke(self):
        r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None,None)
        dao = RelationshipDAO()
        return dao.insertRelationship(r)
    
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

        email = "test42@students.stonehill.edu"
        qrcode = "101010"
        dao = RelationshipDAO()
        
        rc, selectRelationship = dao.selectRelationship(email,qrcode)
        self.assertTrue(rc)
    
    def testSelectRelationshipDoesntExist(self):
        """
        Test that we can't select a relationship that doesnt exist in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        email = "test42@students.stonehill.edu"
        qrcode = "101010"
        dao = RelationshipDAO()
        
        rc, msg = dao.deleteRelationship(email,qrcode)
        self.assertTrue(rc)
        
        rc, selectRelationship = dao.selectRelationship(email,qrcode)
        self.assertFalse(rc)

    def testSelectAllByEmail(self):
        """
        Test that we can select all tuples from one user by email 
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        email = "test42@students.stonehill.edu"
        dao = RelationshipDAO()
        
        rc, selectAllByEmail = dao.selectAllByEmail(email)
        self.assertTrue(rc)

    def testSelectAllByStatus(self):
        """
        Test that we can select all tuples of one status from one user by email 
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        email = "test42@students.stonehill.edu"
        status = "Checked Out"
        dao = RelationshipDAO()
        
        rc, testSelectAllByStatus = dao.selectAllByStatus(email,status)
        self.assertTrue(rc)

    # TEST UPDATE RELATIONSHIP
    def testUpdateRelationship(self):
        """
        Test that we can update a relationship that exists in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","Verified Return",None,None)
        dao = RelationshipDAO()
        
        rc, updateRelationship = dao.updateRelationship(r)
        self.assertTrue(rc)

    # TEST DELETE RELATIONSHIP
    def testDeleteRelationship(self):
        """
        Test that we can delete a relationship that exists in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","Checked Out",None,None)
        dao = RelationshipDAO()
       
        rc, deleteRelationship = dao.deleteRelationship(r)
        self.assertTrue(rc)

if __name__ == '__main__':
    unittest.main()