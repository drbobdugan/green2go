import logging
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
        self.formats = {
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
                }
            
        }

    def getUser(self, request, userDao, hasAuth):
        keys = ["email"]
        return self.userCRUDS(data=[request,keys], userDao=userDao, hasAuth=hasAuth, f=1)

    def getAllUsers(self, request, userDao, hasAuth):
        keys = ["email"]
        return self.userCRUDS(data=[request,keys], userDao=userDao, hasAuth=hasAuth, f=4)

    def addUser(self, request, userDao):
        dictOfUserAttrib = None
        # keys to scape from request
        keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role']
        
        #generate authCode
        authCode=self.helperHandler.genAuthcode()
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, formats=self.formats, hasAuth=False)
            pas=self.helperHandler.encrypt_password(dictOfUserAttrib["password"])
            dictOfUserAttrib["password"]=pas
            dictOfUserAttrib['authCode'] = authCode
            dictOfUserAttrib['authTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dictOfUserAttrib['lastLogIn'] = "None"
            dictOfUserAttrib['authorized'] = "0"
            dictOfUserAttrib['beams_token'] = self.helperHandler.beams_auth(dictOfUserAttrib['email'])
            dictOfUserAttrib['points']="0"
            dictOfUserAttrib['reward_date']= "2021-01-01 01:01:01"
        except Exception as e:
            return json.dumps({"success" : False, "message" :str(e)})
        user = User()
        user.dictToUser(dictOfUserAttrib)
        res = self.userDao.insertUser(user)
        if(res[0] and "/secretAddUser" not in str(request)):
            self.helperHandler.sendEmail(dictOfUserAttrib['email'], dictOfUserAttrib['authCode'])
        return self.helperHandler.handleResponse(res)


    def updateUser(self, request, userDao):
        keys = ['email', 'firstName', 'lastName', 'middleName', 'phoneNum', 'auth_token']
        return self.userCRUDS(data=[request,keys], userDao=userDao, hasAuth=True, f=3)

    def deleteUser(self, request, userDao, hasAuth):
        keys = ['email']
        return self.userCRUDS(data=[request,keys], userDao=userDao, hasAuth=hasAuth, f=2)

    #f values 0->add 1->get 2->delete 3->update 4->getAll
    def userCRUDS(self, data, userDao, hasAuth, f):
        dictOfUserAttrib = None
        request = data[0]
        keys = data[1]
        formats=None
        t= "json"
        isSelectAll=False #remember if request is for select or selectAll
        if f == 1 or f==4:
            t= "args"
        if f==3:
            formats = self.formats
        if f==4:
            isSelectAll=True
        if hasAuth is True and "auth_token" not in keys:
            keys.append('auth_token')
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, formats=formats, hasAuth=hasAuth, t=t)
            if(isSelectAll==True):
                res = self.userDao.selectAll()
                self.helperHandler.falseQueryCheck(res)
                return self.helperHandler.handleResponse(res)
            else:
                res = self.userDao.selectUser(dictOfUserAttrib["email"])
            self.helperHandler.falseQueryCheck(res)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = self.sort(userDao, dictOfUserAttrib, f, res)
        return self.helperHandler.handleResponse(res)


    def sort(self, userDao, d, f, res):
        # get user from table to get missing fields
        user = res[1]
        # convert user obj to dict for simplicity
        UserDic = user.userToDict()
        #get the user from the auth table
        #tempUser = None
        if f == 1: #GET
            UserDic.update({'badges' : UserDic['points'] // 300})
            UserDic.update({'rewardCheck' : self.rewardEligible(UserDic)})
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
    
    def rewardEligible(self, UserDic):
        f='%Y-%m-%d %H:%M:%S'
        rewardTime = UserDic['reward_date']
        if rewardTime == "2021-01-01 01:01:01":
            return False
        authtimets=datetime.strptime(rewardTime, f)
        timepassed=datetime.now()-authtimets
        if (timepassed.total_seconds() / 3600) > 120:
            return False
        else:
            return True

    def changePassword(self, request, userDao):
        userDic = None
        if "/forgetPassword" in str (request):
            keys=['email','newPass', 'auth_token']
        else:
            keys = ['email', 'oldPass', 'newPass', 'auth_token']
        try:
            if "/forgetPassword" in str (request):
                userDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys,hasAuth=False) 
            else:
                userDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys) 
            newPass=self.helperHandler.encrypt_password(userDic["newPass"]) #hash new password
            res = self.userDao.selectUser(userDic['email'])
            self.helperHandler.falseQueryCheck(res)
            user = res[1]
            userAttrib = user.userToDict()
            if "/changePassword" in str (request):
                if not self.helperHandler.check_encrypted_password(userDic['oldPass'], userAttrib['password']):
                    raise Exception("Incorrect password")#check if password is correct
        except Exception as e:
            return json.dumps({"success" : False, "message" :str(e)}) 
        userAttrib['password'] = newPass #set newPass as user Password
        user.dictToUser(userAttrib)
        res = self.userDao.updateUser(user) #Convert to object and update the database
        return self.helperHandler.handleResponse(res)

    def claimReward(self, request, userDao):
        UserDic = None
        keys = ['email', 'auth_token']
        try:
            UserDic = self.helperHandler.handleRequestAndAuth(request = request, keys = keys)
            res = self.userDao.selectUser(UserDic['email'])
            self.helperHandler.falseQueryCheck(res)
        except Exception as e:
            return json.dumps({"success" : False, "message" :str(e)})
        user = res[1]
        UserDic = user.userToDict()
        UserDic['reward_date']= "2021-01-01 01:01:01"
        user.dictToUser(UserDic)
        res = self.userDao.updateUser(user)
        if res[0] == False:
            return json.dumps({"success" : False, "message" :str(e)})
        else:
            return self.helperHandler.handleResponse(res)


