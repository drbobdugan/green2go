import unittest
from locationDao import LocationDao
class unitTestLocationDao(unittest.TestCase):
    """
    Test the locationDao class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestLocationDao.py

    """
    def setUp(self):
        """
        Setup a temporary database
        """

    def tearDown(self):
        """
        Delete the temporary database
        """
        dao = LocationDao()
        locDict={"qrcode": "L042"}
        dao.deleteLocation(locDict)
        del dao
    
    def addTest42Location(self):
        location={
                "qrcode": "L042",
                "description": "Drop-off test location",
                "lastPickup": "2021-01-01 01:01:01"}
        dao = LocationDao()
        return dao.insertLocation(location)
    
    def testRegularAddLocation(self):
        """
        Test that we can add a location that doesn't exist in the database
        """
        rc, msg = self.addTest42Location()
        self.assertTrue(rc)

    def testAddLocationTwice(self):
        """
        Test that we can't add a location twice
        First add should work correctly
        """
        rc, msg = self.addTest42Location()
        self.assertTrue(rc)

        """
        Second add should fail
        """
        rc, msg = self.addTest42Location()
        self.assertFalse(rc)
        self.assertEqual(msg,"Duplicate Entry")
    
    def testRegularSelectLocation(self):
        """
        Test that we can select a location that exists in the database already
        """
        rc, msg = self.addTest42Location()
        self.assertTrue(rc)

        location={"qrcode": "L042"}
        dao = LocationDao()
        rc, selectLocation = dao.selectLocation(location)

        self.assertTrue(rc)
        self.assertEqual(location["qrcode"],selectLocation["qrcode"])
    
    def testSelectLocationDoesntExist(self):
        """
        Test that we can't select a location that doesnt exist in the database already
        """
        rc, msg = self.addTest42Location()
        self.assertTrue(rc)

        location={"qrcode": "L043"}
        dao = LocationDao()
        rc, selectLocation = dao.selectLocation(location)

        self.assertFalse(rc)

if __name__ == '__main__':
    unittest.main()