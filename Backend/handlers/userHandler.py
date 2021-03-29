import json
import string
import random
import sys
import os
from datetime import datetime
sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from userDAO import UserDAO
from user import User
from containerDao import ContainerDao
from authDao import AuthDao
from locationDao import LocationDao

class UserHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler
        self.userDao = UserDAO()

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
            dictOfUserAttrib['authCode'] = authCode
            dictOfUserAttrib['authTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dictOfUserAttrib['lastLogIn'] = "None"
            dictOfUserAttrib['authorized'] = "0"
            dictOfUserAttrib['beams_token'] = "None"
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
        user = User()
        # get user from table to get missing fields
        tempUser = self.userDao.selectUser(d["email"])
        if tempUser[0] is False:
            return False, tempUser[1]
        user = tempUser[1]
        # convert user obj to dict for simplicity
        tempUserDic = user.userToDict()
        print(tempUserDic)
        print(user)
        #tempUser = None
        if f == 1:
            res = [True, tempUserDic]
        elif f == 2:
            self.userDao.deleteUser(user)
            dic = user.userToDict()
            res = [True, dic]
        elif f == 3:
            for key in d:
                tempUserDic[key] = d[key]
            user.dictToUser(tempUserDic)
            self.userDao.updateUser(user)
            dic = user.userToDict()
            res = [True, dic]
        return res

