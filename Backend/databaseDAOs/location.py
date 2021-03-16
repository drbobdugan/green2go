#location object
class Location:
    def __init__(self,location_qrcode,description,lastPickup):
        self.location_qrcode = location_qrcode
        self.description = description
        self.lastPickup = lastPickup
        
    def toString(self):
        return self.location_qrcode + " " + self.description + " " + self.lastPickup