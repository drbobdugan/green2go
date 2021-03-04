import unittest
from containerDao import ContainerDao
class unitTestContainerDao(unittest.TestCase):
    """
    Test the containerDao class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestContainerDao.py
    """

    # make sure to use TEMP database for testing

    def setUp(self):
        """
        Setup a temporary database
        """

    def tearDown(self):
        """
        Delete the temporary database
        """
        dao = ContainerDao()
        containerDict={"qrcode": "101010"}
        relDict={
            "email": "test42@students.stonehill.edu",
            "qrcode": "101010",
            "status": "Checked Out",
            "statusUpdateTime": None
            }
        dao.deleteContainer(containerDict)
        dao.deleteRelationship(relDict)
    
    #container tests include: creating, reading, and deleting
    def addTest42Container(self):
        container={"qrcode": "101010"}
        dao = ContainerDao()
        return dao.addContainer(container)
    
    def testRegularAddContainer(self):
        """
        Test that we can add a container that doesn't exist in the database
        """
        rc, msg = self.addTest42Container()
        self.assertTrue(rc)

    def testAddContainerTwice(self):
        """
        Test that we can't add a container twice
        First add should work correctly
        """
        rc, msg = self.addTest42Container()
        self.assertTrue(rc)

        """
        Second add should fail
        """
        rc, msg = self.addTest42Container()
        self.assertFalse(rc)
        self.assertEqual(msg,"Duplicate Entry")
    
    def testRegularSelectContainer(self):
        """
        Test that we can select a container that exists in the database already
        """
        rc, msg = self.addTest42Container()
        self.assertTrue(rc)

        container={"qrcode": "101010"}
        dao = ContainerDao()
        rc, getContainer = dao.getContainer(container)

        self.assertTrue(rc)
        self.assertEqual(container["qrcode"],getContainer["qrcode"])
    
    def testSelectContainerDoesntExist(self):
        """
        Test that we can't select a container that doesnt exist in the database already
        """
        rc, msg = self.addTest42Container()
        self.assertTrue(rc)

        container={"qrcode": "101010"}
        dao = ContainerDao()
        rc, msg = dao.deleteContainer(container)
        self.assertTrue(rc)
        rc, getContainer = dao.getContainer(container)

        self.assertFalse(rc)
    
    def testDeleteContainer(self):
        """
        Test that we can delete a container from the database
        """
        rc, msg = self.addTest42Container()
        self.assertTrue(rc)

        container={"qrcode": "101010"}
        dao = ContainerDao()
        rc, deleteContainer = dao.deleteContainer(container)

        self.assertTrue(rc)

    # hascontainer tests include: creating, reading, updating, and deleting
    def addTest42Relationship(self):
        rel={
            "email": "test42@students.stonehill.edu",
            "qrcode": "101010",
            "status": "Checked Out",
            "statusUpdateTime": None
            }
        dao = ContainerDao()
        return dao.addRelationship(rel)
    
    def testRegularAddRelationship(self):
        """
        Test that we can add a relationship that doesn't exist in the database
        """
        rc, msg = self.addTest42Relationship()
        self.assertTrue(rc)

    def testAddRelationshipTwice(self):
        """
        Test that we can add a relationship twice
        First add should work correctly
        """
        rc, msg = self.addTest42Relationship()
        self.assertTrue(rc)

        """
        Second add should not fail
        """
        rc, msg = self.addTest42Relationship()
        self.assertTrue(rc)

    def testRegularSelectRelationship(self):
        """
        Test that we can select a relationship that exists in the database already
        """
        rc, msg = self.addTest42Relationship()
        self.assertTrue(rc)

        rel={
            "email": "test42@students.stonehill.edu",
            "qrcode": "101010",
            "status": "Checked Out",
            "statusUpdateTime": None
            }
        dao = ContainerDao()
        rc, getRelationship = dao.getRelationship(rel)

        self.assertTrue(rc)
    
    def testSelectRelationshipDoesntExist(self):
        """
        Test that we can't select a relationship that doesnt exist in the database already
        """
        rc, msg = self.addTest42Relationship()
        self.assertTrue(rc)

        rel={
            "email": "test42@students.stonehill.edu",
            "qrcode": "101010",
            "status": "Checked Out",
            "statusUpdateTime": None
            }
        dao = ContainerDao()
        rc, msg = dao.deleteRelationship(rel)
        self.assertTrue(rc)
        rc, getRelationship = dao.getRelationship(rel)

        self.assertFalse(rc)

    def testUpdateRelationship(self):
        """
        Test that we can update a relationship that exists in the database already
        """
        rc, msg = self.addTest42Relationship()
        self.assertTrue(rc)

        rel={
            "email": "test42@students.stonehill.edu",
            "qrcode": "101010",
            "status": "Pending Return",
            "statusUpdateTime": None
            }
        dao = ContainerDao()
        rc, updateRelationship = dao.updateRelationship(rel)

        self.assertTrue(rc)

    def testDeleteRelationship(self):
        """
        Test that we can delete a relationship that exists in the database already
        """
        rc, msg = self.addTest42Relationship()
        self.assertTrue(rc)

        rel={
            "email": "test42@students.stonehill.edu",
            "qrcode": "101010",
            "status": "Pending Return",
            "statusUpdateTime": None
            }
        dao = ContainerDao()
        rc, deleteRelationship = dao.deleteRelationship(rel)

        self.assertTrue(rc)

if __name__ == '__main__':
    unittest.main()