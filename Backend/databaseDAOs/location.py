#location object
class Location:
    def __init__(self,location_qrcode,description,lastPickup):
        self.location_qrcode = location_qrcode
        self.description = description
        self.lastPickup = lastPickup

    def toLocationList(self):
        locationList = []
        locationList.append(self.location_qrcode)
        locationList.append(self.description)
        locationList.append(self.lastPickup)
        return locationList

    def toLocationDict(self):
        row = dict(location_qrcode=self.location_qrcode, description=self.description,lastPickup=self.lastPickup)
        return row

    def getQRcode(self):
        return self.location_qrcode

    def getDescription(self):
        return self.description

    def getLastPickup(self):
        return self.lastPickup

