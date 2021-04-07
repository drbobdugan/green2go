import re
import json
import string
import random
import sys
import os
from datetime import datetime
sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from userDAO import UserDAO
from authDAO import AuthDao
from auth import Auth
from containerDAO import ContainerDAO
from locationDAO import LocationDao
from emailServer import EmailManager
from pusher_push_notifications import PushNotifications
from pathlib import Path
from pusher_push_notifications import PushNotifications
from passlib.context import CryptContext


class HelperHandler:

    def __init__(self, emailServer):
        self.emailServer = emailServer
        self.authDao = AuthDao()
        self.pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000)

        self.beams_client = PushNotifications(
            instance_id='7032df3e-e5a8-494e-9fc5-3b9f05a68e3c',secret_key='8AC9B8AABB93DFE452B2EFC2714FCF923841B6740F97207F4512F240264FF493')

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
        res = self.authDao.selectByEmail(dic["email"])
        if res[0] is False:
            return False, "No matching user with that authorization token"
        # make sure auth code actually exixts in dattabse
        auth = res[1]
        authDic = auth.authToDict()
        if authDic["auth_token"] != dic["auth_token"]:
            return False, "Invalid token"
        # check that it's not expired
        timeobj=datetime.strptime(authDic["expires_at"], '%Y-%m-%d %H:%M:%S')
        if datetime.now() >= timeobj:
            return False, "Expired token"
        return True, ""

        
    def handleResponse(self, res):
        if res[0] is True:
            return json.dumps({"success" : res[0], "data" : res[1]},default=str)
        else:
            return json.dumps({"success" : res[0], "message" : res[1]})
    
    def beams_auth(self, id):
        beams_token = self.beams_client.generate_token(id)
        return beams_token["token"] 


    def encrypt_password(self,password):
        return self.pwd_context.hash(password)
    def check_encrypted_password(self,password, hashed):
        return self.pwd_context.verify(password, hashed)