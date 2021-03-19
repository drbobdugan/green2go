import json
from userDao import UserDao
from containerDao import ContainerDao
from authDao import AuthDao
from locationDao import LocationDao
from datetime import datetime
from pusher_push_notifications import PushNotifications

class AuthHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler
        self.beams_client = PushNotifications(
            instance_id='1173615',secret_key='f9ffa4761187b1665c2f')

    def validateCode(self, request, userDao, authDao):
        f='%Y-%m-%d %H:%M:%S'
        keys = ["code", "email"]
        dic = None
        try:
            dic = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=False)
        except :
            return json.dumps({"success" : False, "message" : "Please enter a valid code."})
        res=None
        try:
            res = userDao.getUser(dic)
        except:
            res = {"success" : False, "message" : "Email does not correspond to user"}
        codefromtable=res[1]["authCode"]
        authtime=res[1]["authTime"]
        authtimets=datetime.strptime(authtime, f)
        timepassed=datetime.now()-authtimets
        if (dic['code']!=codefromtable):
            return json.dumps({"success" : False, "message" : "Invalid verification code."})
        elif(timepassed.total_seconds()>=300):
            return json.dumps({"success" : False, "message" : "Expired verification code"})
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

    def loginErrorHandler(self, res, dic):
        message = None
        if message is None and "authorized" in res[1] and res[1]["authorized"] == 0:
            message = "Email not found, please try signing up."
        if message is None and "password" in res[1] and dic["password"] != res[1]["password"]:
            message = "Incorrect password."
        return message
            
    def login(self, request, userDao, authDao):
        dic = None
        keys = ["email", "password"]
        try:
            dic = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=False)
        except:
            return json.dumps({"success" : False, "message" : "Please enter an email and password."})
        #get user
        res = userDao.getUser(dic)
        # if not succesful then return why
        if res[0] is False:
            return json.dumps({"success" : res[0], "message" : res[1]})
        # handle login errors
        errorRes = self.loginErrorHandler(res, dic)
        if errorRes is not None:
            return json.dumps({"success" : False, "message" : errorRes})
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

    def beams_auth(self):
        beams_token = self.beams_client.generate_token("test0@students.stonehill.edu")
        return json.dumps(beams_token)
            
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
        if (timepassed.total_seconds()>300):
            authCode=self.helperHandler.genAuthcode()
            user[1]["authCode"]=authCode
            user[1]["authTime"]=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            userDao.updateUser(user[1])
            self.helperHandler.sendEmail(user[1]['email'], authCode)
            return json.dumps({"success" : True, "data": ""})


        return json.dumps({"success" : False, "message" : "Error in resendAuthCode."})
