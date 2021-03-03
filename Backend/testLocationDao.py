from locationDao import LocationDao
dao = LocationDao()
def main():
    testInsertLocation()
    testSelectLocation()

def testInsertLocation():
    #drop off location 1
    locDict={
                "qrcode": "L001",
                "description": "Drop-off bin outside library",
                "lastPickup": "2021-01-01 01:01:01"}
    dao.insertLocation(locDict)
    #drop off location 2
    locDict={
                "qrcode": "L002",
                "description": "Drop-off bin outside College Center",
                "lastPickup": "2021-01-01 01:01:01"}
    dao.insertLocation(locDict)
    #drop off location 3
    locDict={
                "qrcode": "L003",
                "description": "Drop-off bin outside Shields Science Center",
                "lastPickup": "2021-01-01 01:01:01"}
    dao.insertLocation(locDict)
  
def testSelectLocation():
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