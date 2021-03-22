# CONTAINER OBJECT

class Container:
    def __init__(self,qrcode):
        self.qrcode = qrcode

    def toContainerList(self):
        containerList = []
        containerList.append(self.qrcode)
        return containerList

    def toContainerDict(self):
        dictionary = dict(qrcode=self.qrcode)
        return dictionary

    def getQRcode(self):
        return self.qrcode

    def setQRcode(self,newQRcode):
        self.qrcode=newQRcode