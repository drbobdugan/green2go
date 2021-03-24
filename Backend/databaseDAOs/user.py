class User:
    def __init__(self,email,password,firstName,LastName,middleName,phoneNum,role,classYear,authCode,authTime,lastLogIn,authorized,beams_token):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = LastName
        self.middleName = middleName
        self.phoneNum = phoneNum
        self.role = role
        self.classYear = classYear
        self.authCode = authCode
        self.authTime = authTime
        self.lastLogIn = lastLogIn
        self.authorized = authorized
        self.beams_token= beams_token
    def userToList(self):
        return (self.email,self.password,self.firstName,self.lastName,self.middleName,self.phoneNum,self.role,self.classYear,self.authCode,self.authTime,self.lastLogIn,self.authorized,self.beams_token)
    def userToDict(self):
        return {"email": self.email,"password": self.password,"firstName": self.firstName,"lastName": self.lastName,"middleName": self.middleName,"phoneNum": self.phoneNum,"role": self.role,"classYear": self.classYear,"authCode": self.authCode,"authTime": self.authTime,"lastLogIn": self.lastLogIn,"authorized":self.authorized,"beams_token":self.beams_token}