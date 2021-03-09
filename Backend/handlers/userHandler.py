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

    def getUser(self, request, userDao, containerDao):
        #TODO split up errors
        dictOfUserAttrib = None
        keys = ["email", "auth_token"]
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res=userDao.getUser(dictOfUserAttrib)
        if res[0] is False:
            return json.dumps({"success" : res[0], "message" : res[1]})
        response = containerDao.selectAllByEmail(dictOfUserAttrib)
        return self.handleResponse(res)

    def addUser(self, request, userDao):
        dictOfUserAttrib = None
        # keys to scape from request
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear']
        formats = {'email' : "([a-zA-Z0-9_.+-]+@+((students\.stonehill\.edu)|(stonehill\.edu))$)"}
        #generate authCode
        authCode=self.helperHandler.id_generator()
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, formats=formats, hasAuth=False)
            dictOfUserAttrib["authCode"] = authCode
        except Exception as e:
            return json.dumps({"success" : False, "message" :"Please complete all fields to sign up."})
        res = userDao.addUser(dictOfUserAttrib)
        return self.handleResponse(res)

    def updateUser(self, request, userDao):
        dictOfUserAttrib = None
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear', 'authCode', 'auth_token']
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = userDao.updateUser(dictOfUserAttrib)
        return self.handleResponse(res)

    def deleteUser(self, request, userDao):
        dictOfUserAttrib = None
        keys = ['email', 'auth_token']
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = userDao.deleteUser(dictOfUserAttrib)
        return self.handleResponse(res)

    def handleResponse(self, res):
        if res[0] is True:
            return json.dumps({"success" : res[0], "data" : res[1]})
        else:
            return json.dumps({"success" : res[0], "message" : res[1]})

