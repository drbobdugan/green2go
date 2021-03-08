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

# this crates the unique code for the user 
    def id_generator(self, size=12, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

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
        if response[0] is True:
            res = {"success" : res[0], "data" : {"user" : res[1], "containers" : response[1]}}
        else:
            res = {"success" : response[0], "message" : response[1]}    
        return json.dumps(res) 

    def addUser(self, request, userDao):
        dictOfUserAttrib = None
        # keys to scape from request
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear']
        formats = {'email' : "([a-zA-Z0-9_.+-]+@+((students\.stonehill\.edu)|(stonehill\.edu))$)"}
        #generate authCode
        authCode=self.id_generator()
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, formats=formats, hasAuth=False)
            dictOfUserAttrib["authCode"] = authCode
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = userDao.addUser(dictOfUserAttrib)
        if res[0] is True:
            self.helperHandler.sendEmail(request.json['email'], authCode)
            return json.dumps({"success" : res[0], "data" : ""})
        else:
            return json.dumps({"success" : res[0], "message" : res[1]})

    def updateUser(self, request, userDao):
        dictOfUserAttrib = None
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear', 'authCode', 'auth_token']
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = userDao.updateUser(dictOfUserAttrib)
        print(res)
        if res [0] is True:
            return json.dumps({"success" : res[0], "message" : ""})
        else:
            return json.dumps({"success" : res[0], "message" : res[1]})

    def deleteUser(self, request, userDao):
        dictOfUserAttrib = None
        keys = ['email', 'auth_token']
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = userDao.deleteUser(dictOfUserAttrib)
        if res[0] is True:
            return json.dumps({"success" : res[0], "message" : ""})
        else:
            return json.dumps({"success" : res[0], "message" : res[1]})

