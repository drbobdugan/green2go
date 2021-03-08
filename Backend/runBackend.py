from flask import Flask
import mysql.connector
import json
import string
import random
from flask import request
from userDao import UserDao
from containerDao import ContainerDao
from authDao import AuthDao
from locationDao import LocationDao
from datetime import datetime
import sys
import os
import re
import logging
sys.path.insert(0, os.getcwd()+'/Email/')
from emailServer import EmailManager

#app methods
app = Flask(__name__)
app.debug = True

#daos and objects
userDao=UserDao()
containerDao=ContainerDao()
authDao = AuthDao()
locationDao=LocationDao()
emailServer = EmailManager()


#----------------------------Helper Methods --------------------------------

#returns [true|false, ""|exception]
def handleRequestAndAuth(request, keys, required=None ,t="json", formats=None, hasAuth=True):
    # format dictionary from request correctly
    dic = None
    try:
        dic = extractKeysFromRequest(request, keys, required ,t)
    except Exception as e:
        raise Exception(str(e).replace("'", '') + " field missing from request")
    # Ensure correct formatting
    if formats is None:
        pass
    else:
        try:
            ensureCorrectFormatting(dic, formats)
        except Exception as e:
            raise Exception(str(e).replace("'", ''))
    if hasAuth is True:
    # Ensure Authorized Request
        authCheck = handleAuth(dic)
        print(authCheck)
        if authCheck[0] is False:
            raise Exception(authCheck[1])
    return dic

    
# only called once dicOfValues has been verified by extractKeysFromRquest
def ensureCorrectFormatting(dicOfValues, formats):
    for key in dicOfValues:
        if dicOfValues[key] is None:
            pass
        else:
            if not re.match(formats[key], dicOfValues[key]):
                raise Exception(str(key) + " does not match specified format")

    return True

def extractKeysFromRequest(request, keys, required=None ,t="json"):
    if required is None:
        required = keys
    if t == "json":
        dic = {key : request.json[key] if key in request.json else None for key in keys}
        for key in required:
            if dic[key] is None:
                raise Exception(key)
        return dic
    elif t == "args":
        dic = {key : request.args.get(key) for key in keys}
        for key in required:
            if dic[key] is None:
                raise Exception(key)
        return dic
    return None

def handleAuth(dic):
    res = authDao.getAuth(dic)
    if res[0] is True:
        # make sure auth code actually exixts in dattabse
        if res[1]["auth_token"] != dic["auth_token"]:
            return False, "Invalid token"
        # check that it's not expired
        timeobj=datetime.strptime(res[1]["expires_at"], '%Y-%m-%d %H:%M:%S')
        if datetime.now() >= timeobj:
            return False, "Expired token"
        return True, ""
    else:
        return False, "No matching user with that authorization token"

#----------------------------Email Methods --------------------------------
def sendEmail(email, code):
    global emailServer
    return emailServer.sendEmail(email, code)

#----------------------------Validity Methods --------------------------------
@app.route('/validateCode', methods=['POST'])
def validateCode():
    f='%Y-%m-%d %H:%M:%S'
    keys = ["code", "email"]
    dic = None
    try:
        dic = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global userDao

    res=None

    try:
        res = userDao.getUser(dic)
    except:
        res = {"success" : False, "message" : "Email does not correspond to user"}
    codefromtable=res[1]["authCode"]
    authtime=res[1]["authTime"]
    authtimets=datetime.strptime(authtime, f)
    timepassed=datetime.now()-authtimets
    if (dic['code']==codefromtable and timepassed.total_seconds()<300):
        # delete previous auth
        try:
            authDao.deleteAuth(res[1])
        except:
            pass
        # create new auth
        res = authDao.addAuth(res[1])
        # fix userAuth as well
        userDao.updateUser({"email" : dic["email"], "authorized" : 1})
        # return it
        return json.dumps({"success" : res[0], "data" : res[1]})
    else:
        return json.dumps({"success" : False, "message" : "Expired token"})

@app.route('/login', methods=['POST'])
def login():
    dic = None
    keys = ["email", "password"]
    try:
        dic = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global userDao

    res = None
    try:
        res = userDao.getUser(dic)
    except:
        return json.dumps({"success" : res[0], "message" : res[1]})

    if "authorized" in res[1] and res[1]["authorized"] == 0:
        return json.dumps({"success" : False, "message" : "Registration not complete"})

    if "password" in res[1] and dic["password"] == res[1]["password"]:
        # delete previous auth
        try:
            authDao.deleteAuth(dic)
        except:
            pass
        # create new auth
        res = authDao.addAuth(dic)
        # return it
        return json.dumps({"success" : res[0], "data" : res[1]})
    else:
        return json.dumps({"success" : False, "message" : "Incorrect password"})

@app.route('/auth/refresh', methods=['POST'])
def refreshCode():
    dic = None
    keys = ["email", "refresh_token"]
    try:
        dic = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    res = authDao.getAuth(dic)
    if res[0] is True:
        # refresh token mismatch
        if dic["refresh_token"] != res[1]["refresh_token"]:
            return json.dumps({"success" : False, "mesage":"Invalid token"})
        # handle is auth code is expired
        timeobj=datetime.strptime(res[1]["expires_at"], '%Y-%m-%d %H:%M:%S')
        if datetime.now() >= timeobj:
            return json.dumps({"success" : False, "message":"Expired token"})
        # return normal response
        updated = authDao.updateAuth(dic)
        return json.dumps({"success" : True, "data": updated[1]})
    else:
        return json.dumps({"success" : False, "message" : "Invalid refresh token"})


@app.route('/resendAuthCode',methods=['POST'])
def resendAuthCode():
    f='%Y-%m-%d %H:%M:%S'
    authCode=None
    dictOfUserAttrib = None
    keys = ["email","auth_token"]
    dic=None
    try:
         dic = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    authCheck = handleAuth(dic)
    if authCheck[0] is False:
        return json.dumps({"success" : False, "message" : authCheck[1]})
    global userDao
    user=None
    try:
        user = userDao.getUser(dic)
    except:
        user = {"success" : False, "message" : "Email does not correspond to user"}
    #print(user[1]['authTime'])
    authtime=user[1]["authTime"]
    authtimets=datetime.strptime(authtime, f)
    timepassed=datetime.now()-authtimets
    if(timepassed.total_seconds()<300):
        sendEmail(user[1]['email'], user[1]['authCode'])
        return json.dumps({"success" : True, "data": ""})
    else:
        authCode=id_generator()
        sendEmail(user[1]['email'], authCode)
        user[1]["authCode"]=authCode
        user[1]["authTime"]=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res = userDao.updateUser(user[1])
        if res [0] is True:
            return json.dumps({"success" : res[0], "message" : ""})
        else:
            return json.dumps({"success" : res[0], "message" : res[1]})

#----------------------------User Methods --------------------------------
# this crates the unique code for the user 
def id_generator(size=12, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/getUser', methods=['GET'])
def getUser():
    dictOfUserAttrib = None
    keys = ["email", "auth_token"]
    try:
        dictOfUserAttrib = handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})
    global userDao
    res=userDao.getUser(dictOfUserAttrib)
    if res[0] is True:
        response = containerDao.selectAllByEmail(dictOfUserAttrib)
        if response[0] is True:
            res = {"success" : res[0], "data" : {"user" : res[1], "containers" : response[1]}}
        else:
            res = {"success" : response[0], "message" : response[1]}
    else:
        res = {"success" : res[0], "message" : res[1]}
    return json.dumps(res) 

@app.route('/addUser', methods=['POST'])
def addUser():
    dictOfUserAttrib = None
    # keys to scape from request
    keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear']
    formats = {'email' : "([a-zA-Z0-9_.+-]+@+((students\.stonehill\.edu)|(stonehill\.edu))$)"}
    #generate authCode
    authCode=id_generator()
    try:
        dictOfUserAttrib = handleRequestAndAuth(request=request, keys=keys, formats=formats, hasAuth=False)
        dictOfUserAttrib["authCode"] = authCode
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})
    global userDao
    res = userDao.addUser(dictOfUserAttrib)
    if res[0] is True:
        sendEmail(request.json['email'], authCode)
        return json.dumps({"success" : res[0], "data" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})


@app.route('/updateUser', methods=['PATCH'])
def updateUser():
    dictOfUserAttrib = None
    keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear', 'authCode', 'auth_token']
    try:
        dictOfUserAttrib = handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})
    global userDao
    res = userDao.updateUser(dictOfUserAttrib)
    print(res)
    if res [0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})

@app.route('/deleteUser', methods=['DELETE'])
def deleteUser():
    dictOfUserAttrib = None
    keys = ['email', 'auth_token']
    try:
        dictOfUserAttrib = handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})
    global userDao
    res = userDao.deleteUser(dictOfUserAttrib)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})


#----------------------------Container Methods --------------------------------

#currently wrap the container qrcode in list because that's how db handles is in  DAO
@app.route('/addContainer', methods=['POST'])
def addContainer():
    containerDic = None
    keys = ["qrcode"]
    try:
        containerDic = handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})
    global containerDao
    res = containerDao.addContainer(containerDic)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})

@app.route('/getContainer', methods = ['GET'])
def getContainer():
    containerDic = None
    keys = ["qrcode", "auth_token", "email"]
    try:
        containerDic = handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})
    global containerDao
    res = containerDao.getContainer(containerDic)
    if res[0] is True:
        res = json.dumps({"success" : res[0], "data" : res[1]})
    else:
        res = json.dumps({"success" : res[0], "message" : res[1]})
    return res

@app.route('/deleteContainer', methods = ['DELETE'])
def deleteContainer():
    containerDic = None
    keys = ["qrcode", "auth_token", "email"]
    try:
        containerDic = handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})
    global containerDao
    res = containerDao.deleteContainer(containerDic)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})


@app.route('/updateContainer', methods=['PATCH'])
def updateContainer():
    containerDic = None
    keys = ['qrcode', "auth_token", "email"]
    try:
        containerDic = handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})
    global containerDao
    res = containerDao.updateContainer(containerDic)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})

#----------------------------HasContainer Methods --------------------------------

#TODO: Need to update logic in all these methods

#Accepts list val in format  val = (email, qrcode, status, statusUpdateTime)
@app.route('/checkoutContainer', methods=['POST'])
def checkoutContainer():
    userContainer = None
    keys=['email','qrcode','status'] # ask the database team if they are check for pendings that will switch to returned for older user
    try:
        userContainer = handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})
    global containerDao
    res = containerDao.addRelationship(userContainer)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})

@app.route('/getContainersForUser', methods = ['GET'])
def getContainersForUser():
    relationship = None
    keys=['email','auth_token']
    try:
        relationship = handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
        if relationship is None:
            raise Exception("relationship")
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e)})

    authCheck = handleAuth(relationship)
    if authCheck[0] is False:
        return json.dumps({"success" : False, "message" : authCheck[1]})
    relationship.pop('auth_token', None)
    global containerDao
    res = containerDao.selectAllByEmail(relationship)
    if res[0] is True:
        res = json.dumps({"success" : res[0], "data" : res[1]})
    else:
        res = json.dumps({"success" : res[0], "message" : res[1]})
    return res

@app.route('/checkinContainer', methods=['POST'])
def checkinContainer():  # we are going to do loction than the container so get loction for the front end here
    dictOfUserAttrib = None
    keys = ['email', 'qrcode', 'status', 'statusUpdateTime']

    dictOfUserAttrib = extractKeysFromRequest(request, keys)
    global containerDao
    res = containerDao.updateRelationship(dictOfUserAttrib)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})

#----------------------------Location Methods --------------------------------
    
@app.route('/selectLocation',methods=['POST'])
def selectLoction():
    locationDic = None
    keys = ["qrcode",'email','auth_token']
    try:
        locationDic = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global containerDao
    authCheck = handleAuth(locationDic)
    if authCheck[0] is False:
        return json.dumps({"success" : False, "message" : authCheck[1]})
    locationDic.pop('auth_token', None)
    res = locationDao.selectLocation(locationDic)  #need to get the method for database team 
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
