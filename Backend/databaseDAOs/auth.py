#auth object
class Auth:
    def __init__(self, *args):
        if args != ():
            self.listToAuth(args)

    def authToList(self):
        return(self.user,self.auth_token,self.refresh_token,self.expires_at)

    def listToAuth(self,list):
        self.user = list[0]
        self.auth_token = list[1]
        self.refresh_token = list[2]
        self.expires_at = list[3]

    def dictToAuth(self,dict):
        self.listToAuth((dict["user"],dict["auth_token"],dict["refresh_token"],dict["expires_at"]))

    def authToDict(self):
        return {"user": self.user, "auth_token": self.auth_token, "refresh_token": self.refresh_token, "expires_at": str(self.expires_at)}

    def getUser(self):
        return self.user

    def getAuthToken(self):
        return self.auth_token

    def getRefreshToken(self):
        return self.refresh_token

    def getExpiresAt(self):
        return self.expires_at