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
        self.dao = LocationDao()
        loc = Location("L042","Drop-off bin outside Testing Center","2021-01-01 01:01:01") # loc is location object 
        self.dao.deleteLocation(loc)
    
    # test creating location
    def testInsertLocationSmoke(self):
        loc = Location("L042","Drop-off bin outside Testing Center","2021-01-01 01:01:01") 
        self.dao = LocationDao()
        return self.dao.insertLocation(loc)
    
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

    def testInsertLocationNoneType(self):
        loc = Location(None,"Drop-off bin outside Testing Center","2021-01-01 01:01:01") 
        self.dao = LocationDao()

        rc, insertLocation = self.dao.insertLocation(loc)
        self.assertFalse(rc)

        loc = Location("L043",None,"2021-01-01 01:01:01")
        rc, insertLocation = self.dao.insertLocation(loc)
        self.assertFalse(rc)

        loc = Location("L043","Drop-off bin outside Testing Center",None)
        rc, insertLocation = self.dao.insertLocation(loc)
        self.assertFalse(rc)

    def testselectByLocationQRcode(self):
        """
        Test that we can select a location that exists in the database already
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertTrue(rc)

        qrcode = "L042"
        self.dao = LocationDao()
        rc, selectByLocationQRcode = self.dao.selectByLocationQRcode(qrcode)

        self.assertTrue(rc)
        self.assertEqual(qrcode,selectByLocationQRcode.location_qrcode)
    
    def testselectByLocationQRcodeDoesntExist(self):
        """
        Test that we can't select a location that doesnt exist in the database already
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertTrue(rc)

        qrcode = "L043"
        self.dao = LocationDao()
        rc, selectByLocationQRcode = self.dao.selectByLocationQRcode(qrcode)

        self.assertFalse(rc)
        rc, selectByLocationQRcode = self.dao.selectByLocationQRcode(None)

        self.assertFalse(rc)
        
    def testDeleteLocation(self):
        """
        Test that we can delete a location from the database
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertTrue(rc)

        loc = Location("L042","Drop-off bin outside Testing Center","2021-01-01 01:01:01") 
        self.dao = LocationDao()
        
        rc, deleteLocation = self.dao.deleteLocation(loc)
        self.assertTrue(rc)

        rc, selectLocation = self.dao.selectByLocationQRcode("L042")
        self.assertFalse(rc)
    
    def testDeleteLocationDoesntExist(self):
        """
        Test that we can't delete a location that doesn't exist
        """
        rc, msg = self.testInsertLocationSmoke()
        self.assertTrue(rc)

        loc = Location("L043","Drop-off bin outside Roche Commons","2021-01-01 01:01:01") 
        self.dao = LocationDao()

        rc, deleteLocation = self.dao.deleteLocation(loc)
        self.assertFalse(rc)

        rc, deleteLocation = self.dao.deleteLocation(None)
        self.assertFalse(rc)

    def testInsertLocationQRCodeTooLong(self):
        """
        Test that we cannot add a location_qrcode that is over 45 characters long
        """
        loc = Location("L043xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","Drop-off bin outside Roche Commons","2021-01-01 01:01:01") 
        self.dao = LocationDao()

        rc, insertLocation = self.dao.insertLocation(loc)
        self.assertFalse(rc)

    def testInsertDescriptionTooLong(self):
        """
        Test that we cannot add a description that is over 128 characters long
        """
        loc = Location("L042",
        "Drop-off bin outside Roche Commons xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "2021-01-01 01:01:01") 
        self.dao = LocationDao()

        rc, insertLocation = self.dao.insertLocation(loc)
        self.assertFalse(rc)

    def testInsertWrongDate(self):
        """
        Test that we cannot add a incorrectly formatted date
        """
        loc = Location("L042","Drop-off bin outside Roche Commons","01:01:01 2021-01-01") 
        self.dao = LocationDao()

        rc, insertLocation = self.dao.insertLocation(loc)
        self.assertFalse(rc)

if __name__ == '__main__':
    unittest.main()
    
