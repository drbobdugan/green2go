#location object
class Location:
    def __init__(self, *args):
        if args != ():
            self.listToLocation(args)
    
    def locationToList(self):
        return (self.location_qrcode,self.description,self.lastPickup)

    def listToLocation(self,list):
        self.location_qrcode = list[0]
        self.description = list[1]
        self.lastPickup = list[2]

    def dictToLocation(self,dict):
        self.listToLocation((dict["location_qrcode"],dict["description"],dict["lastPickup"]))

    def locationToDict(self):
        return {"location_qrcode": self.location_qrcode,"description": self.description,"lastPickip": self.lastPickup}
