import json
import string
import random
from datetime import datetime
from userDao import UserDao
from containerDao import ContainerDao
from authDao import AuthDao
from locationDao import LocationDao

class UserHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler

    def getUser(self, request, userDao, containerDao, hasAuth):
        keys = ["email"]
        return self.userCRUDS(request=request, userDao=userDao, containerDao=containerDao, hasAuth=hasAuth, keys=keys, function=1)

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
        except Exception as e:
            return json.dumps({"success" : False, "message" :str(e)})
        res = userDao.addUser(dictOfUserAttrib)
        print(res)
        if(res[0]):
            self.helperHandler.sendEmail(dictOfUserAttrib['email'], dictOfUserAttrib['authCode'])
        return self.helperHandler.handleResponse(res)


    def updateUser(self, request, userDao):
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear', 'authCode', 'auth_token']
        return self.userCRUDS(request=request, userDao=userDao, containerDao=None, hasAuth=hasAuth, keys=keys, function=3)

    def deleteUser(self, request, userDao, hasAuth):
        keys = ['email']
        return self.userCRUDS(request=request, userDao=userDao, containerDao=None, hasAuth=hasAuth, keys=keys, function=2)

    #function values 0->add 1->get 2->delete 3->update
    def userCRUDS(self, request, userDao, containerDao, hasAuth, keys, function):
        dictOfUserAttrib = None
        if hasAuth is True and "auth_token" not in keys:
            keys.append('auth_token')
        try:
            if function == 0 or function == 2 or function == 3:
                dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=hasAuth)
            else:
                dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=hasAuth, t="args")
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        if function == 1:
            res = userDao.getUser(dictOfUserAttrib)
        elif function == 2:
            res = userDao.deleteUser(dictOfUserAttrib)
        elif function == 3:
            res = userDao.updateUser(dictOfUserAttrib)
        return self.helperHandler.handleResponse(res)

