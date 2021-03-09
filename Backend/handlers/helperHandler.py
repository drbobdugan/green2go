import re
import json
import string
import random
from datetime import datetime
from userDao import UserDao
from containerDao import ContainerDao
from authDao import AuthDao
from locationDao import LocationDao
from emailServer import EmailManager

class HelperHandler:

    def __init__(self, emailServer):
        self.emailServer = emailServer

    # this crates the unique code for the user 
    def id_generator(self, size=12, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    #returns [true|false, ""|exception]
    def handleRequestAndAuth(self, request, keys, required=None ,t="json", formats=None, hasAuth=True):
        # format dictionary from request correctly
        dic = None
        try:
            dic = self.extractKeysFromRequest(request, keys, required ,t)
        except Exception as e:
            raise Exception(str(e).replace("'", '') + " field missing from request")
        # Ensure correct formatting
        try:
            self.ensureCorrectFormatting(dic, formats)
        except Exception as e:
            raise Exception(str(e).replace("'", ''))
        if hasAuth is False:
            return dic
        # Ensure Authorized Request
        authCheck = self.handleAuth(dic)
        if authCheck[0] is False:
            raise Exception(authCheck[1])
        return dic

    def sendEmail(self, email, code):
        return self.emailServer.sendEmail(email, code)

        
    # only called once dicOfValues has been verified by extractKeysFromRquest
    def ensureCorrectFormatting(self, dicOfValues, formats):
        print(formats)
        if formats is None:
            return True
        for key in formats:
            if dicOfValues[key] is not None and (not re.match(formats[key], dicOfValues[key])):
                raise Exception("Please enter a valid "+str(key)+".")
        return True

    def extractKeysFromRequest(self, request, keys, required=None ,t="json"):
        dic = {}
        if required is None:
            required = keys
        for key in keys:
            dic[key] = None
            if t == "json":
                if key in request.json:
                    dic[key] = request.json[key]
            elif t == "args":
                dic[key] = request.args.get(key)
        for key in required:
            if dic[key] is None:
                raise Exception(key)
        return dic

    def handleAuth(self, dic):
        authDao = AuthDao()
        res = authDao.getAuth(dic)
        del authDao
        if res[0] is False:
            return False, "No matching user with that authorization token"
        # make sure auth code actually exixts in dattabse
        if res[1]["auth_token"] != dic["auth_token"]:
            return False, "Invalid token"
        # check that it's not expired
        timeobj=datetime.strptime(res[1]["expires_at"], '%Y-%m-%d %H:%M:%S')
        if datetime.now() >= timeobj:
            return False, "Expired token"
        return True, ""