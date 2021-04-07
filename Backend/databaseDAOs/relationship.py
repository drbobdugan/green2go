# RELATIONSHIP OBJECT

class Relationship:
    def __init__(self, *args):
        if args != ():
            self.listToRelationship(args)

    # list to object
    def listToRelationship(self,list):
        self.email = list[0]
        self.qrcode = list[1]
        self.status = list[2]
        self.statusUpdateTime = list[3]
        self.location_qrcode = list[4]
        self.active = list[5]
        self.description = list[6]
    
    # object to list
    def relationshipToList(self):
        return(self.email,self.qrcode,self.status,self.statusUpdateTime,self.location_qrcode,self.active,self.description)
    
    # dictionary to object
    def dictToRelationship(self,dict):
        self.listToRelationship((dict["email"],dict["qrcode"],dict["status"],dict["statusUpdateTime"],dict["location_qrcode"],dict['active'],dict["description"]))

    # object to dictionary
    def relationshipToDict(self):
        return {"email":self.email,"qrcode":self.qrcode,"status":self.status,"statusUpdateTime":self.statusUpdateTime,"location_qrcode":self.location_qrcode,"active":self.active,"description":self.description}