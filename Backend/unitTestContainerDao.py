import unittest
from containerDao import ContainerDao
class unitTestContainerDao(unittest.TestCase):
    """
    Test the containerDao class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestContainerDao.py
    """
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
        dao.deleteContainer(containerDict)
    
    #container tests include: adding and getting // do we need deleting?
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
        rc, getContainer = dao.getContainer(qrcode)

        self.assertFalse(rc)

    # hascontainer tests include: creating, reading, and updating
    def addTest42Relationship(self):
        rel={
            "email": "test42@students.stonehill.edu",
            "qrcode": "101010",
            "status": "Checked Out";
            "statusUpdateTime": "2021-01-01 01:01:01"
            }
        dao = ContainerDao()
        return dao.addRelationship(rel)
    
    def testRegularAddRelationship(self):

    def testAddRelationshipTwice(self):
    
    def testRegularSelectRelationship(self):
    
    def testSelectRelationshipDoesntExist(self):

    def testUpdateRelationship(self):

if __name__ == '__main__':
    unittest.main()