import json
import string
import random
import sys
import os
from datetime import datetime
sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from userDAO import UserDAO
from user import User
from authDAO import AuthDao
from auth import Auth

class UserHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler
        self.userDao = UserDAO()
        self.authDao = AuthDao()

    def getUser(self, request, userDao, hasAuth):
        keys = ["email"]
        return self.userCRUDS(data=[request,keys], userDao=userDao, hasAuth=hasAuth, f=1)

    def addUser(self, request, userDao):
        dictOfUserAttrib = None
        # keys to scape from request
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear']
        formats = {
            'email' : {
                "format":"([a-zA-Z0-9_.+-]+@+((students\.stonehill\.edu)|(stonehill\.edu))$)",
                "error":"Email"
                },
            'password' : {
                "format":"(([a-z|A-Z|0-9])|([^A-Za-z0-9]))+$",
                "error":"Password"
                },
            'firstName': {
                "format":"[a-z|A-Z]+$",
                "error":"First Name"
                },
            'lastName': {
                "format":"[a-z|A-Z]+$",
                "error":"Last Name"
                },
            'middleName': {
                "format":"[a-z|A-Z]*$",
                "error":"Middle Name"
                },
            'phoneNum': {
                "format":"([0-9]{10}$)|([0-9]{11}$)|([0-9]{12}$)",
                "error":"Phone Number"
                },
            'role': {
                "format":"(RegularUser$)|(Admin$)",
                "error":"Role"
                },
            'classYear': {
                "format":"(19[0-9]{2}$)|(20[0-2]{1}[0-9]{1}$)",
                "error":"Class Year"
                }
            
        }
        #generate authCode
        authCode=self.helperHandler.genAuthcode()
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, formats=formats, hasAuth=False)
            pas=self.helperHandler.encrypt_password(dictOfUserAttrib["password"])
            dictOfUserAttrib["password"]=pas
            dictOfUserAttrib['authCode'] = authCode
            dictOfUserAttrib['authTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dictOfUserAttrib['lastLogIn'] = "None"
            dictOfUserAttrib['authorized'] = "0"
            dictOfUserAttrib['beams_token'] = self.helperHandler.beams_auth(dictOfUserAttrib['email'])
        except Exception as e:
            return json.dumps({"success" : False, "message" :str(e)})
        user = User()
        user.dictToUser(dictOfUserAttrib)
        res = self.userDao.insertUser(user)
        if(res[0]):
            self.helperHandler.sendEmail(dictOfUserAttrib['email'], dictOfUserAttrib['authCode'])
        return self.helperHandler.handleResponse(res)


    def updateUser(self, request, userDao):
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear', 'authCode', 'auth_token']
        return self.userCRUDS(data=[request,keys], userDao=userDao, hasAuth=True, f=3)

    def deleteUser(self, request, userDao, hasAuth):
        keys = ['email']
        return self.userCRUDS(data=[request,keys], userDao=userDao, hasAuth=hasAuth, f=2)

    #f values 0->add 1->get 2->delete 3->update
    def userCRUDS(self, data, userDao, hasAuth, f):
        dictOfUserAttrib = None
        request = data[0]
        keys = data[1]
        t= "json"
        if f == 1:
            t= "args"
        if hasAuth is True and "auth_token" not in keys:
            keys.append('auth_token')
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=hasAuth, t=t)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = self.sort(userDao, dictOfUserAttrib, f)
        return self.helperHandler.handleResponse(res)

    def sort(self, userDao, d, f):
        res = None
        # get user from table to get missing fields
        res = self.userDao.selectUser(d["email"])
        user = res[1]
        if res[0] is False:
            return False, res[1]
        # convert user obj to dict for simplicity
        UserDic = user.userToDict()
        #get the user from the auth table
        #tempUser = None
        if f == 1: #GET
            res = [True, UserDic]
        elif f == 2: #DELETE: delete user and auth
            try:
                res = self.authDao.selectByEmail(d["email"])
                auth = res[1]
                self.authDao.deleteAuth(auth)
            except:
                pass
            self.userDao.deleteUser(user)
            dic = user.userToDict()
            res = [True, dic]
        elif f == 3: #UPDATE: update dic, convert to user, and update user table
            for key in d:
                UserDic[key] = d[key]
            user.dictToUser(UserDic)
            self.userDao.updateUser(user)
            res = [True, UserDic]
        return res

