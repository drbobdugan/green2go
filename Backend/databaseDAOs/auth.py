#auth object
class Auth:
    def __init__(self,user,auth_token,refresh_token,expires_at):
        self.user = user
        self.auth_token = auth_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def toAuthList(self):
        authList = []
        authList.append(self.user)
        authList.append(self.auth_token)
        authList.append(self.refresh_token)
        authList.append(self.expires_at)
        return authList

    def toAuthDict(self):
        row = dict(user=self.user, auth_token=self.auth_token,refresh_token=self.refresh_token,expires_at=self.expires_at)
        return row

    def getUser(self):
        return self.user

    def getAuthToken(self):
        return self.auth_token

    def getRefreshToken(self):
        return self.refresh_token

    def getExpiresAt(self):
        return self.expires_at