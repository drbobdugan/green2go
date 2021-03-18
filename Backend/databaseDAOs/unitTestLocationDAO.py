import unittest
from location import Location
from locationDAO import LocationDao

class unitTestLocationDAO(unittest.TestCase):
    """
    Test the locationDAO class methods using the unit test framework.  
    To run these tests:
         python3 -m unittest unitTestLocationDAO.py
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
        loc = Location("L042","Drop-off bin outside Testing Center","2021-01-01 01:01:01") # loc is location object 
        dao.deleteLocation(loc)
    
    # test creating location
    def testInsertLocationSmoke(self):
        loc = Location("L042","Drop-off bin outside Testing Center","2021-01-01 01:01:01") 
        dao = LocationDao()
        return dao.insertLocation(loc)
    
    def testInsertLocation(self):
        """
        Test that we can add a location that doesn't exist in the database
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertTrue(rc)

    def testInsertLocationTwice(self):
        """
        Test that we can't add a location twice
        First add should work correctly
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertTrue(rc)

        """
        Second add should fail
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertFalse(rc)
        self.assertEqual(msg,"Duplicate Entry")

    def testselectByLocationQRcode(self):
        """
        Test that we can select a location that exists in the database already
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertTrue(rc)

        qrcode = "L042"
        dao = LocationDao()
        rc, selectByLocationQRcode = dao.selectByLocationQRcode(qrcode)

        self.assertTrue(rc)
        self.assertEqual(qrcode,selectByLocationQRcode.location_qrcode)
    
    def testselectByLocationQRcodeDoesntExist(self):
        """
        Test that we can't select a location that doesnt exist in the database already
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertTrue(rc)

        qrcode = "L043"
        dao = LocationDao()
        rc, selectByLocationQRcode = dao.selectByLocationQRcode(qrcode)

        self.assertFalse(rc)

    def testDeleteLocation(self):
        """
        Test that we can delete a location from the database
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertTrue(rc)

        loc = Location("L042","Drop-off bin outside Testing Center","2021-01-01 01:01:01") 
        dao = LocationDao()
        
        rc, deleteLocation = dao.deleteLocation(loc)
        self.assertTrue(rc)


if __name__ == '__main__':
    unittest.main()
    
