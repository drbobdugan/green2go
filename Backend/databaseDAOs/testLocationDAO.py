from location import Location
from locationDAO import LocationDao
dao = LocationDao()

def main():
    #testInsertLocation()
    testSelectByLocationQRcode()

def testInsertLocation():
    #drop off location 1
    location= Location("L001","Drop-off bin outside library","2021-01-01 01:01:01")
    dao.insertLocation(location)
    #drop off location 2
    location = Location("L002","Drop-off bin outside College Center","2021-01-01 01:01:01")
    dao.insertLocation(location)
    #drop off location 4
    location = Location("L004","Drop-off bin outside Holy Cross Center","2021-01-01 01:01:01")
    dao.insertLocation(location)
  
def testSelectByLocationQRcode():
    #location 1
    qrcode = "L001"
    print(dao.selectByLocationQRcode(qrcode))
    #location 2
    qrcode = "L002"
    print(dao.selectByLocationQRcode(qrcode))
    #location 3
    qrcode = "L004"
    print(dao.selectByLocationQRcode(qrcode))

main()