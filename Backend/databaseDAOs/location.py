#location object
class Location:
    def __init__(self,location_qrcode,description,lastPickup):
        self.location_qrcode = location_qrcode
        self.description = description
        self.lastPickup = lastPickup
    
    def toLocationObject(self):
        location = Location(self.location_qrcode, self.description, self.lastPickup)
        return location

    def toLocationList(self):
        location = Location(self.location_qrcode, self.description, self.lastPickup)
        locationList = []
        locationList.append(location.location_qrcode)
        locationList.append(location.description)
        locationList.append(location.lastPickup)
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

