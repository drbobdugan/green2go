# CONTAINER OBJECT

class Container:
    def __init__(self, *args):
        if args != ():
            self.listToContainer(args)

    # list to object
    def listToContainer(self,list):
        self.qrcode = list[0]
       
    # object to list
    def containerToList(self):
        containerList = []
        containerList.append(self.qrcode)
        return containerList

    # dictionary to object
    def dictToContainer(self,dict):
        self.qrcode = dict["qrcode"]

    # object to dictionary
    def containerToDict(self):
        return {"qrcode": self.qrcode}
        
    # getters and setters
    def getQRcode(self):
        return self.qrcode
    def setQRcode(self,newQRcode):
        self.qrcode=newQRcode