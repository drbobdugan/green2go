import json
import os
import sys
sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from userDAO import UserDAO
from containerDAO import ContainerDAO
from authDAO import AuthDao
from locationDAO import LocationDao
from user import User
from container import Container
from auth import Auth
from location import Location
from datetime import datetime
from pusher_push_notifications import PushNotifications

class AuthHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler
        self.beams_client = PushNotifications(
            instance_id='7032df3e-e5a8-494e-9fc5-3b9f05a68e3c',secret_key='8AC9B8AABB93DFE452B2EFC2714FCF923841B6740F97207F4512F240264FF493')
        self.userDao = UserDAO()
        self.containerDao = ContainerDAO()
        self.authDao = AuthDao()
        self.locationDao = LocationDao()

    def validateCode(self, request, userDao, authDao):
        f='%Y-%m-%d %H:%M:%S'
        keys = ["code", "email"]
        dic = None
        try:
            dic = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=False)
        except :
            return json.dumps({"success" : False, "message" : "Please enter a valid code."})
        user = User()
        res = self.userDao.selectUser(dic["email"])
        user = res[1]
        if res[0] is False:
            return json.dumps({"success" : False, "message" : "Email does not correspond to user"})
        userDic = user.userToDict()
        codefromtable=userDic["authCode"]
        authtime=userDic["authTime"]
        authtimets=datetime.strptime(authtime, f)
        timepassed=datetime.now()-authtimets
        if (dic['code']!=codefromtable):
            return json.dumps({"success" : False, "message" : "Invalid verification code."})
        elif(timepassed.total_seconds()>=300):
            return json.dumps({"success" : False, "message" : "Expired verification code"})
        # create new auth
        authDic = {}
        authDic["user"] = dic["email"]
        authDic["auth_token"] = self.helperHandler.id_generator(size=45)
        authDic["refresh_token"] = self.helperHandler.id_generator(size=45)
        authDic["expires_at"] = ""
        auth = Auth()
        auth.dictToAuth(authDic)
        self.authDao.deleteAuth(auth)
        res = self.authDao.insertAuth(auth)
        data = auth.authToDict()
        # fix userAuth as well
        userDic["authorized"] = "1"
        user.dictToUser(userDic)
        userDao.updateUser(user)
        # return it
        return json.dumps({"success" : res[0], "data" : data})

    def loginErrorHandler(self, userDic, dic):
        message = None
        dencryptedpas=self.helperHandler.check_encrypted_password(dic["password"],userDic["password"])
        print(dencryptedpas)
        if message is None and "authorized" in userDic and userDic["authorized"] == 0:
            message = "Email not found, please try signing up."
        if message is None and dencryptedpas ==False:
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
        res = self.userDao.selectUser(dic["email"])
        # if not succesful then return why
        if res[0] is False:
            return json.dumps({"success" : res[0], "message" : res[1]})
        # handle login errors
        user = res[1]
        userDic = user.userToDict()
        errorRes = self.loginErrorHandler(userDic, dic)
        print(errorRes)
        if errorRes is not None:
            return json.dumps({"success" : False, "message" : errorRes})
        # retrieve auth
        res = self.authDao.selectByEmail(dic["email"])
        if res[0] is False:
            return json.dumps({"success" : res[0], "message" : res[1]})
        auth = res[1]
        # update the auth
        authDic = auth.authToDict()
        authDic["auth_token"] = self.helperHandler.id_generator(size=45)
        authDic["refresh_token"] = auth.refresh_token
        auth.dictToAuth(authDic)
        res = self.authDao.updateAuth(auth)
        auth = res[1]
        # return it
        return json.dumps({"success" : res[0], "data" : auth.authToDict()})
            
    def refreshCode(self, request, authDao):
        dic = None
        keys = ["email", "refresh_token"]
        try:
            dic = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=False)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = self.authDao.selectByEmail(dic["email"])
        auth = res[1]
        message = None
        if res[0] is False:
            message = "Invalid refresh token"
        # refresh token mismatch
        authDic = auth.authToDict()
        if dic["refresh_token"] != authDic["refresh_token"]:
            message = "Invalid token"
        # handle is auth code is expired
        timeobj=datetime.strptime(authDic["expires_at"], '%Y-%m-%d %H:%M:%S')
        if datetime.now() >= timeobj:
            message = "Expired token"
        if message is not None:
            return json.dumps({"success" : False, "message": message})
        # return normal response
        authDic["token"] = self.helperHandler.id_generator(size=45)
        auth.dictToAuth(authDic)
        res = self.authDao.updateAuth(auth)
        return json.dumps({"success" : True, "data": authDic})

    def beams_auth(self, param):
        beams_token = self.beams_client.generate_token(param)
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
        
        user=User()
        user = self.userDao.selectUser(dic["email"])
        if user[0] == False:
            return json.dumps({"success" : user[0], "message": user[1]})
        authtime=user[1].authTime
        authtimets=datetime.strptime(authtime, f)
        timepassed=datetime.now()-authtimets
        if(timepassed.total_seconds()<300):
            self.helperHandler.sendEmail(user[1].email, user[1].authCode)
            return json.dumps({"success" : True, "data": ""})
        if (timepassed.total_seconds()>300):
            authCode=self.helperHandler.genAuthcode()
            user[1].authCode=authCode
            user[1].authTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            userdic=user[1].userToDict()
            
            self.userDao.updateUser(user[1])
            self.helperHandler.sendEmail(user[1].email, authCode)
            return json.dumps({"success" : True, "data": ""})


        return json.dumps({"success" : False, "message" : "Error in resendAuthCode."})
