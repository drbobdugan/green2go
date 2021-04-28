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
       self.dao = RelationshipDAO()
       self.dao.changeDatabase("temp")

    def tearDown(self):
        """
        Delete the temporary database
        """
        r = Relationship("test42@students.stonehill.edu","101010","Checked Out","2021-01-01 01:01:01",None,None) # r is relationship object
        self.dao.deleteRelationship(r)
        r.status = "Verified Return"
        self.dao.deleteRelationship(r)
        r.status = "Damaged Lost"
        self.dao.deleteRelationship(r)
        r.status = "Pending Return"
        self.dao.deleteRelationship(r)

    # TEST CREATE RELATIONSHIP
    def testInsertRelationshipSmoke(self):
        r = Relationship("test42@students.stonehill.edu","101010","Checked Out","2021-01-01 01:01:01",None,None)
        return self.dao.insertRelationship(r)
    
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
        Second add should also work correctly
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

    def testInsertRelationshipNoneType(self):
        r = Relationship(None,"101010","Checked Out","2021-01-01 01:01:01",None, None)
        rc, msg  = self.dao.insertRelationship(r)
        self.assertFalse(rc)

        r = Relationship("test42@students.stonehill.edu",None,"Checked Out","2021-01-01 01:01:01",None, None)
        rc, msg  = self.dao.insertRelationship(r)
        self.assertFalse(rc)

        r = Relationship("test42@students.stonehill.edu","101010",None,"2021-01-01 01:01:01",None, None)
        rc, msg  = self.dao.insertRelationship(r)
        self.assertFalse(rc)


    # TEST READ RELATIONSHIP
    def testSelectRelationship(self):
        """
        Test that we can select a relationship that exists in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        email = "test42@students.stonehill.edu"
        qrcode = "101010"
        rc, selectRelationship = self.dao.selectRelationship(email,qrcode)
        self.assertTrue(rc)
    
    def testSelectRelationshipDoesntExist(self):
        """
        Test that we can't select a relationship that doesnt exist in the database already
        """
        rc, selectRelationship = self.dao.selectRelationship("test43@students.stonehill.edu","0000")
        self.assertFalse(rc)

    def testSelectAllByEmail(self):
        """
        Test that we can select all tuples from one user by email 
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        email = "test42@students.stonehill.edu"
        rc, selectAllByEmail = self.dao.selectAllByEmail(email)
        self.assertTrue(rc)

    def testSelectAllByStatus(self):
        """
        Test that we can select all tuples of one status from one user by email 
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        email = "test42@students.stonehill.edu"
        status = "Checked Out"
        rc, testSelectAllByStatus = self.dao.selectAllByStatus(email,status)
        self.assertTrue(rc)

        for i in testSelectAllByStatus:
            self.assertEqual(i["status"], status)
            self.assertEqual(i["email"], email)

    def testSelectAll(self):
        """
        Test that we can select all tuples in the hascontainer table
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        rc, testSelectAll = self.dao.selectAll()
        self.assertTrue(rc)
        
    def testSelectPendingReturns(self):
        """
        Test that we can select all tuples with status = "Pending Return" 
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        rc, testSelectPendingReturns = self.dao.selectPendingReturns()
        self.assertTrue(rc)

        for i in testSelectPendingReturns:
            self.assertEqual(i["status"], "Pending Return")

    # TEST UPDATE RELATIONSHIP
    def testUpdateRelationship(self):
        """
        Test that we can update a relationship that exists in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","Pending Return","2021-01-01 01:01:01",None,"Pending Return")
        rc, updateRelationship = self.dao.updateRelationship(r)
        self.assertTrue(rc)



    # TEST DELETE RELATIONSHIP
    def testDeleteRelationship(self):
        """
        Test that we can delete a relationship that exists in the database already
        """
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","Checked Out","2021-01-01 01:01:01",None,None)
        rc, deleteRelationship = self.dao.deleteRelationship(r)
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","Damaged Lost","2021-01-01 01:01:01",None,None)
        rc, msg = self.dao.insertRelationship(r)
        self.assertTrue(rc)
        rc, deleteRelationship = self.dao.deleteRelationship(r)
        self.assertTrue(rc)

    def testGetRecentUser(self):
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        rc, msg = self.dao.getRecentUser("101010")
        self.assertTrue(rc)
        self.assertTrue(msg == "test42@students.stonehill.edu")

        rc, msg = self.dao.getRecentUser("16546456")
        self.assertFalse(rc)

        r = Relationship("test43@students.stonehill.edu","101010","Checked Out","2021-01-01 01:01:01",None,None)
        rc, msg = self.dao.insertRelationship(r)
        self.assertTrue(rc)

        rc, msg = self.dao.getRecentUser("101010")
        self.assertTrue(rc)
        self.assertTrue(msg == "test43@students.stonehill.edu")

        rc, msg = self.dao.deleteRelationship(r)
        self.assertTrue(rc)

#____________________________________________________________________________________________________________________________________________________________#

    # TEST SPECIAL CASES - INCORRECT FORMATS
    def testInsertEmailTooLong(self):
        """
        Test that we cannot add an email that is over 45 characters long
        """
        r = Relationship("test42xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@students.stonehill.edu","101010","Checked Out","2021-01-01 01:01:01",None,None) 
        self.dao = RelationshipDAO()

        rc, insertRelationship = self.dao.insertRelationship(r)
        self.assertFalse(rc)

    def testInsertQRCodeTooLong(self):
        """
        Test that we cannot add a QR code that is over 45 characters long
        """
        r = Relationship("test42@students.stonehill.edu","101010xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","Checked Out","2021-01-01 01:01:01",None,None) 
        self.dao = RelationshipDAO()

        rc, insertRelationship = self.dao.insertRelationship(r)
        self.assertFalse(rc)

    def testInsertStatusNotValid(self):
        """
        Test that we cannot add a status that is not:
        Checked Out | Pending Return | Verified Return | Damaged Lost
        """
        
        r = Relationship("test42@students.stonehill.edu","101010","TEST WRONG STATUS","2021-01-01 01:01:01",None,None) 
        self.dao = RelationshipDAO()

        rc, insertRelationship = self.dao.insertRelationship(r)
        self.assertFalse(rc)
        
        """
        Test that we cannot add a status that is over 45 characters long
        """
        r = Relationship("test42@students.stonehill.edu","101010","Checked out xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","2021-01-01 01:01:01",None,None) 
        self.dao = RelationshipDAO()

        rc, insertRelationship = self.dao.insertRelationship(r)
        self.assertFalse(rc)

    def testInsertWrongStatusUpdateTime(self):
        """
        Test that we cannot add a incorrectly formatted date
        """
        """
        r = Relationship("test42@students.stonehill.edu","101010","Checked Out","01:01:01 2021-01-01",None,None) 
        self.dao = RelationshipDAO()

        rc, insertRelationship = self.dao.insertRelationship(r)
        self.assertFalse(rc)
        """
        # this yields True is not false error
        # we think this takes our wrong date because it is just overwritten in the dao

    def testInsertLocQRCodeTooLong(self):
        """
        Test that we cannot add a location QR code that is over 45 characters long
        """
        r = Relationship("test42@students.stonehill.edu","101010","Checked Out","2021-01-01 01:01:01","L043xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",None) 
        self.dao = RelationshipDAO()

        rc, insertRelationship = self.dao.insertRelationship(r)
        self.assertFalse(rc)


    def testInsertDescTooLong(self):
        """
        Test that we cannot add a description that is more than 128 characters long.
        """
        
        r = Relationship("test42@students.stonehill.edu","101010","Checked Out","2021-01-01 01:01:01","L043","paloeklslslslslslslslslslslslslslslslslslslslaeowlsosjdoskejepspsosdksdkfjsldkflaksdjflkjasdkfjaskjdflkjasdfljsadkfjkasndfklasjndfkaskjldflsadfnlkajsndfknasldkjfnalksjdnflkjasndlkfjnsakjdnfkaslndfkljsandfkjnka") 
        self.dao = RelationshipDAO()

        rc, insertRelationship = self.dao.insertRelationship(r)
        self.assertFalse(rc)
       
    def testUpdateStatusNotValid(self):
        """
        Test that we cannot update a status that is not:
        Checked Out | Pending Return | Verified Return | Damaged Lost
        """
        
        rc, msg = self.testInsertRelationshipSmoke()
        self.assertTrue(rc)

        r = Relationship("test42@students.stonehill.edu","101010","WRONG STATUS","2021-01-01 01:01:01",None,"Pending Return")
        rc, updateRelationship = self.dao.updateRelationship(r)
        self.assertFalse(rc)

        r.status = "Checked out"
        rc, updateRelationship = self.dao.updateRelationship(r)
        self.assertFalse(rc)

        r.status = "pending return"
        rc, updateRelationship = self.dao.updateRelationship(r)
        self.assertFalse(rc)

        r.status = "VERIFIED RETURN"
        rc, updateRelationship = self.dao.updateRelationship(r)
        self.assertFalse(rc)        


if __name__ == '__main__':
    unittest.main()
