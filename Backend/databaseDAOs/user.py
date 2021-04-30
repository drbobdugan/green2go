class User:
    def __init__(self, *args):
        if args != ():
            self.listToUser(args)

    def userToList(self):
        return (self.email,
                self.password,
                self.firstName,
                self.lastName,
                self.middleName,
                self.phoneNum,
                self.role,
                self.authCode,
                self.authTime,
                self.lastLogIn,
                self.authorized,
                self.beams_token,
                self.points)

    def listToUser(self,list):
        self.email = list[0]
        self.password = list[1]
        self.firstName = list[2]
        self.lastName = list[3]
        self.middleName = list[4]
        self.phoneNum = list[5]
        self.role = list[6]
        self.authCode = list[7]
        self.authTime = list[8]
        self.lastLogIn = list[9]
        self.authorized = list[10]
        self.beams_token = list[11]
        self.points = list[12]
        
    def dictToUser(self,dict):
        self.listToUser((dict["email"],
                        dict["password"],
                        dict["firstName"],
                        dict["lastName"],
                        dict["middleName"],
                        dict["phoneNum"],
                        dict["role"],
                        dict["authCode"],
                        dict["authTime"],
                        dict["lastLogIn"],
                        dict["authorized"],
                        dict["beams_token"],
                        dict["points"]))

    def userToDict(self):
        return {"email": self.email,
                "password": self.password,
                "firstName": self.firstName,
                "lastName": self.lastName,
                "middleName": self.middleName,
                "phoneNum": self.phoneNum,
                "role": self.role,
                "authCode": self.authCode,
                "authTime": self.authTime,
                "lastLogIn": self.lastLogIn,
                "authorized":self.authorized,
                "beams_token":self.beams_token,
                "points": self.points}