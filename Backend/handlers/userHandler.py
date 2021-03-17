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
        #TODO split up errors
        dictOfUserAttrib = None
        keys = ["email"]
        if hasAuth is True:
            keys.append("auth_token")
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=hasAuth)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res=userDao.getUser(dictOfUserAttrib)
        if res[0] is False:
            return json.dumps({"success" : res[0], "message" : res[1]})
        response = containerDao.selectAllByEmail(dictOfUserAttrib)
        return self.helperHandler.handleResponse(res)

    def addUser(self, request, userDao):
        dictOfUserAttrib = None
        # keys to scape from request
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear']
        formats = {
            'email' : "([a-zA-Z0-9_.+-]+@+((students\.stonehill\.edu)|(stonehill\.edu))$)",
            'password' : "[a-z|A-Z]+$",
            'firstName': "[a-z|A-Z]+$",
            'lastName': "[a-z|A-Z]+$",
            'middleName': "[a-z|A-Z]*$",
            'phoneNum': "([0-9]{10}$)|([0-9]{11}$)|([0-9]{12}$)",
            'role': "(RegularUser$)|(Admin$)",
            'classYear': "(19[0-9]{2}$)|(20[0-2]{1}[0-9]{1}$)"
            
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
        dictOfUserAttrib = None
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear', 'authCode', 'auth_token']
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = userDao.updateUser(dictOfUserAttrib)
        return self.helperHandler.handleResponse(res)

    def deleteUser(self, request, userDao, hasAuth):
        dictOfUserAttrib = None
        keys = ['email']
        if hasAuth is True:
            keys.append('auth_token')
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=hasAuth)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = userDao.deleteUser(dictOfUserAttrib)
        return self.helperHandler.handleResponse(res)

