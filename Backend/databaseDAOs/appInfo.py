# CONTAINER OBJECT

class appInfo:
    def __init__(self, *args):
        if args != ():
            self.listToAppInfo(args)

    # list to object
    def listToAppInfo(self,list):
        self.major = list[0]
        self.minor = list[1]
        self.patch = list[2]
        self.host = list[3]
       
    # object to list
    def appInfoToList(self):
        return [self.major,self.minor,self.patch,self.host]

    # dictionary to object
    def dictToAppInfo(self,dict):
        self.major = dict["major"]
        self.minor = dict["minor"]
        self.patch = dict["patch"]
        self.host = dict["host"]

    # object to dictionary
    def appInfoToDict(self):
        return {"major": self.major,"minor":self.minor,"patch":self.patch,"host":self.host}