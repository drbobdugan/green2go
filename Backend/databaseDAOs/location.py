#location object
class Location:
    def __init__(self,location_qrcode,description,lastPickup):
        self.location_qrcode = location_qrcode
        self.description = description
        self.lastPickup = lastPickup
    
    def toLocationList(self):
        location = Location(self.location_qrcode, self.description, self.lastPickup)
        return location

    def toLocationDict(self):
        row = dict(location_qrcode=self.location_qrcode, description=self.description,lastPickup=self.lastPickup)
        return row


    #add getQRcode
    
