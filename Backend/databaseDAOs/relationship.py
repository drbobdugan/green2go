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
    
    # object to list
    def relationshipToList(self):
        return(self.email,self.qrcode,self.status,self.statusUpdateTime,self.location_qrcode)
    
    # dictionary to object
    def dictToRelationship(self,dict):
        self.listToRelationship((dict["email"],dict["qrcode"],dict["status"],dict["statusUpdateTime"],dict["location_qrcode"]))

    # object to dictionary
    def relationshipToDict(self):
        return {"email":self.email,"qrcode":self.qrcode,"status":self.status,"statusUpdateTime":self.statusUpdateTime,"location_qrcode":self.location_qrcode}

    # getters and setters
    def getEmail(self):
        return self.email
    def setEmail(self,newEmail):
        self.email=newEmail
    def getQRcode(self):
        return self.qrcode
    def setQRcode(self,newQRcode):
        self.qrcode=newQRcode
    def getStatus(self):
        return self.status
    def setStatus(self,newStatus):
        self.status=newStatus
    def getStatusUpdateTime(self):
        return self.statusUpdateTime
    def setStatusUpdateTime(self,newTime):
        self.statusUpdateTime=newTime
    def getLocQRcode(self):
        return self.location_qrcode
    def setLocQRcode(self,newLocQRcode):
        self.location_qrcode=newLocQRcode