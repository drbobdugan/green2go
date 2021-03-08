import json
from userDao import UserDao
from containerDao import ContainerDao
from authDao import AuthDao
from locationDao import LocationDao

class AuthHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler

    def validateCode(self, request, userDao, authDao):
        f='%Y-%m-%d %H:%M:%S'
        keys = ["code", "email"]
        dic = None
        try:
            dic = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=False)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res=None
        try:
            res = userDao.getUser(dic)
        except:
            res = {"success" : False, "message" : "Email does not correspond to user"}
        codefromtable=res[1]["authCode"]
        authtime=res[1]["authTime"]
        authtimets=datetime.strptime(authtime, f)
        timepassed=datetime.now()-authtimets
        if (dic['code']!=codefromtable or timepassed.total_seconds()>=300):
            return json.dumps({"success" : False, "message" : "Expired token"})
        # delete previous auth
        try:
            authDao.deleteAuth(res[1])
        except:
            pass
        # create new auth
        res[1]["auth_token"] = self.helperHandler.id_generator(size=45)
        res[1]["refresh_token"] = self.helperHandler.id_generator(size=45)
        res = authDao.addAuth(res[1])
        # fix userAuth as well
        userDao.updateUser({"email" : dic["email"], "authorized" : 1})
        # return it
        return json.dumps({"success" : res[0], "data" : res[1]})
            
    def login(self, request, userDao, authDao):
        dic = None
        keys = ["email", "password"]
        try:
            dic = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=False)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = userDao.getUser(dic)
        if "authorized" in res[1] and res[1]["authorized"] == 0:
            return json.dumps({"success" : False, "message" : "Registration not complete"})
        if "password" in res[1] and dic["password"] != res[1]["password"]:
            return json.dumps({"success" : False, "message" : "Incorrect password"})
        # delete previous auth
        try:
            authDao.deleteAuth(dic)
        except:
            pass
        # create new auth
        dic["auth_token"] = self.helperHandler.id_generator(size=45)
        dic["refresh_token"] = self.helperHandler.id_generator(size=45)
        res = authDao.addAuth(dic)
        # return it
        return json.dumps({"success" : res[0], "data" : res[1]})
            
    def refreshCode(self, request, authDao):
        dic = None
        keys = ["email", "refresh_token"]
        try:
            dic = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=False)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = authDao.getAuth(dic)
        message = None
        if res[0] is False:
            message = "Invalid refresh token"
        # refresh token mismatch
        if dic["refresh_token"] != res[1]["refresh_token"]:
            message = "Invalid token"
        # handle is auth code is expired
        timeobj=datetime.strptime(res[1]["expires_at"], '%Y-%m-%d %H:%M:%S')
        if datetime.now() >= timeobj:
            message = "Expired token"
        if message is not None:
            return json.dumps({"success" : False, "message": message})
        # return normal response
        dic["token"] = self.helperHandler.id_generator(size=45)
        updated = authDao.updateAuth(dic)
        return json.dumps({"success" : True, "data": updated[1]})
            
    def resendAuthCode(self, request, userDao, authDao):
        f='%Y-%m-%d %H:%M:%S'
        authCode=None
        dictOfUserAttrib = None
        keys = ["email","auth_token"]
        dic=None
        try:
            dic = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=False)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        user=None
        try:
            user = userDao.getUser(dic)
        except:
            user = {"success" : False, "message" : "Email does not correspond to user"}
        authtime=user[1]["authTime"]
        authtimets=datetime.strptime(authtime, f)
        timepassed=datetime.now()-authtimets
        if(timepassed.total_seconds()<300):
            self.helperHandler.sendEmail(user[1]['email'], user[1]['authCode'])
            return json.dumps({"success" : True, "data": ""})
        return json.dumps({"success" : res[0], "message" : res[1]})
