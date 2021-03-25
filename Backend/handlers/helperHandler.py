import re
import json
import string
import random
import sys
import os
from datetime import datetime
from userDao import UserDao
from authDao import AuthDao
from containerDao import ContainerDao
#sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
#from authDAO import AuthDao
from locationDao import LocationDao
from emailServer import EmailManager
from pathlib import Path

class HelperHandler:

    def __init__(self, emailServer):
        self.emailServer = emailServer

    # this crates the unique code for the user 
    def id_generator(self, size=12, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def genAuthcode(self):
        authcode=""
        for i in range (0,6):
            authcode= authcode + random.choice(string.digits)
        return authcode
            
    def extractQRCodesFromFile(self, p="../../qrCodes/qrCodes.txt"):
        path = Path(__file__).parent / p
        codesFile = path.open()
        lines = codesFile.readlines()
        codesFile.close()
        codes = []
        for line in lines:
            codes.append(line.split(':')[1].strip())
        return codes

    def getValidLocationCodes(self):
        return ['L001', 'L002', 'L003', 'L004']


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
        if formats is None:
            return True
        for key in formats:
            if dicOfValues[key] is not None and (not re.match(formats[key]["format"], dicOfValues[key])):
                raise Exception("Please enter a valid "+str(formats[key]["error"])+".")
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

        
    def handleResponse(self, res):
        if res[0] is True:
            return json.dumps({"success" : res[0], "data" : res[1]},default=str)
        else:
            return json.dumps({"success" : res[0], "message" : res[1]})