from locationDAO import LocationDAO
import location
dao = LocationDao()
def main():
    testInsertLocation()
    testSelectLocation()

def testInsertLocation():
    #drop off location 1
    location= Location("L001","Drop-off bin outside library","2021-01-01 01:01:01")
    dao.insertLocation(location)
    #drop off location 2
    location = Location("L002","Drop-off bin outside College Center","2021-01-01 01:01:01")
    dao.insertLocation(location)
    #drop off location 3
    locDict={
                "qrcode": "L003",
                "description": "Drop-off bin outside Shields Science Center",
                "lastPickup": "2021-01-01 01:01:01"}
    dao.insertLocation(locDict)
  
def testSelectByLocationQRcode():
    #location 1
    qrcode = "L001"
    locDict={"qrcode": qrcode}
    print(dao.selectLocation(locDict))
    #location 2
    qrcode = "L002"
    contDict={"qrcode": qrcode}
    print(dao.selectLocation(locDict))
    #location 3
    qrcode = "L003"
    contDict={"qrcode": qrcode}
    print(dao.selectLocation(locDict))

main()