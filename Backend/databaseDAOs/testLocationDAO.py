from location import Location
from locationDAO import LocationDao
dao = LocationDao()

def main():
    """
    Uncomment the desired method to test it
    """
    testSelectAll()
    #testSelectByLocationQRcode()
    #testInsertLocation()
    #testDeleteLocation()
    
def testSelectAll():
    print(dao.selectAll()) #returns all locations as objects

def testSelectByLocationQRcode():
    #location 1
    qrcode = "L001"
    print(dao.selectByLocationQRcode(qrcode)) #returns specific location object selected by location_qrcode
    #location 2
    qrcode = "L002"
    print(dao.selectByLocationQRcode(qrcode))
    #location 3
    qrcode = "L004"
    print(dao.selectByLocationQRcode(qrcode))

def testInsertLocation():
    #drop off location 1
    location= Location("L001","Drop-off bin outside library","2021-01-01 01:01:01")
    #dao.insertLocation(location)
    #drop off location 2
    location = Location("L002","Drop-off bin outside College Center","2021-01-01 01:01:01")
    #dao.insertLocation(location)
    #drop off location 4
    location = Location("L005","Drop-off bin outside TEST","2021-01-01 01:01:01")
    dao.insertLocation(location)

def testDeleteLocation():
    location = Location("L005","Drop-off bin outside TEST","2021-01-01 01:01:01")
    dao.deleteLocation(location)

main()