# RELATIONSHIP OBJECT

class Relationship:
    def __init__(self,email,qrcode,status,statusUpdateTime,location_qrcode):
        self.email = email
        self.qrcode = qrcode
        self.status = status
        self.statusUpdateTime = statusUpdateTime
        self.location_qrcode = location_qrcode

    def toRelationshipList(self):
        return (self.email,self.qrcode,self.status,self.statusUpdateTime,self.location_qrcode)

    def toRelationshipDict(self):
        return {"email":self.email,"qrcode":self.qrcode,"status":self.status,"statusUpdateTime":self.statusUpdateTime,"location_qrcode":self.location_qrcode}

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