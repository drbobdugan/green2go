from flask import Flask
import mysql.connector
import json
import string
import random
from flask import request
from userDao import UserDao
from containerDao import ContainerDao
from authDao import AuthDao
from datetime import datetime
import sys
import os
import re
sys.path.insert(0, os.getcwd()+'/Email/')
from emailServer import EmailManager
app = Flask(__name__)
dao=UserDao()
dao2=ContainerDao()
authDao = AuthDao()

emailServer = EmailManager()

#----------------------------Helper Methods --------------------------------

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

def validateEmail(email):
    if not re.match("([a-zA-Z0-9_.+-]+@+((students\.stonehill\.edu)|(stonehill\.edu))$)", email):
        return False
    return True

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
    global dao

    res=None

    try:
        res = dao.getUser(dic)
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
        dao.updateUser({"email" : dic["email"], "authorized" : 1})
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
    global dao

    res = None
    try:
        res = dao.getUser(dic)
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
        return json.dumps({"success" : "False", "message" : "Incorrect password"})

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

#----------------------------User Methods --------------------------------
# this crates the unique code for the user 
def id_generator(size=12, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/getUser', methods=['GET'])
def getUser():
    dictOfUserAttrib = None
    keys = ["email", "auth_token"]
    try:
        dictOfUserAttrib = extractKeysFromRequest(request, keys, t="args")
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao
    
    authCheck = handleAuth(dictOfUserAttrib)
    if authCheck[0] is False:
        return json.dumps({"success" : False, "message" : authCheck[1]})

    res=dao.getUser(dictOfUserAttrib)
    #print(res)
    if res[0] is True:
        res = {"success" : res[0], "data" : res[1]}
    else:
        res = {"success" : res[0], "message" : res[1]}
    return json.dumps(res) 

@app.route('/addUser', methods=['POST'])
def addUser():
    dictOfUserAttrib = None
    # keys to scape from request
    keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear']
    authCode=id_generator()
    try:
        dictOfUserAttrib = extractKeysFromRequest(request, keys)
        dictOfUserAttrib["authCode"] = authCode
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
         
    if validateEmail(dictOfUserAttrib["email"]) is False:
        return json.dumps({"success" : False, "message" : "Invalid email format"})

    global dao
    res = dao.addUser(dictOfUserAttrib)
    #print(res)
    if res[0] is True:
        # send email
        sendEmail(request.json['email'], authCode)
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})


@app.route('/updateUser', methods=['PATCH'])
def updateUser():
    dictOfUserAttrib = None
    keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear', 'authCode', 'auth_token']
    try:
        dictOfUserAttrib = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao

    authCheck = handleAuth(dictOfUserAttrib)
    if authCheck[0] is False:
        return json.dumps({"success" : False, "message" : authCheck[1]})
    # take auth_token out of dict for database team
    dictOfUserAttrib.pop('auth_token', None)
    res = dao.updateUser(dictOfUserAttrib)
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
        dictOfUserAttrib = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})

    authCheck = handleAuth(dictOfUserAttrib)
    if authCheck[0] is False:
        return json.dumps({"success" : False, "message" : authCheck[1]})

    global dao
    res = dao.deleteUser(dictOfUserAttrib)
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
        containerDic = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao2
    res = dao2.addContainer(containerDic)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})

@app.route('/getContainer', methods = ['GET'])
def getContainer():
    containerDic = None
    keys = ["qrcode", "auth_token", "email"]
    try:
        containerDic = extractKeysFromRequest(request, keys, t="args")
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao2

    authCheck = handleAuth(containerDic)
    if authCheck[0] is False:
        return json.dumps({"success" : False, "message" : authCheck[1]})

    res = dao2.getContainer(containerDic)
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
        containerDic = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao2

    authCheck = handleAuth(containerDic)
    if authCheck[0] is False:
        return json.dumps({"success" : False, "message" : authCheck[1]})

    res = dao2.deleteContainer(containerDic)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})


@app.route('/updateContainer', methods=['PATCH'])
def updateContainer():
    containerDic = None
    keys = ['qrcode', "auth_token", "email"]
    try:
        containerDic = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})

    authCheck = handleAuth(containerDic)
    if authCheck[0] is False:
        return json.dumps({"success" : False, "message" : authCheck[1]})

    # take auth_token out of dict for database team
    containerDic.pop('auth_token', None)

    global dao2
    res = dao2.updateContainer(containerDic)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})

#----------------------------HasContainer Methods --------------------------------

#Accepts list val in format  val = (email, qrcode, status, statusUpdateTime)
@app.route('/addRelationship', methods=['POST'])
def addRelationship():
    userContainer = None
    keys=['email','qrcode','status']
    try:
        userContainer = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao2
    res = dao2.addRelationship(userContainer)
    print(res)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})
@app.route('/getRelationship', methods = ['GET'])
def getRelationship():
    relationship = None
    keys=['email','qrcode']
    try:
        relationship = extractKeysFromRequest(request, keys, t="args")
        if relationship is None:
            raise Exception("relationship")
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao2
    res = dao2.getRelationship(relationship)
    if res[0] is True:
        res = json.dumps({"success" : res[0], "message" : ""})
    else:
        res = json.dumps({"success" : res[0], "message" : res[1]})
    return res

@app.route('/updateRelationship', methods=['PATCH'])
def updateRelationship():
    dictOfUserAttrib = None
    keys = ['email', 'qrcode', 'status', 'statusUpdateTime']

    dictOfUserAttrib = extractKeysFromRequest(request, keys)
    global dao2
    res = dao2.updateRelationship(dictOfUserAttrib)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})

@app.route('/deleteRelationship', methods=['DELETE'])
def deleteRelationship():
    relationship = None
    keys=['email','qrcode','status']
    try:
        relationship = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao2
    res = dao2.deleteRelationship(relationship)
    if res[0] is True:
        return json.dumps({"success" : res[0], "message" : ""})
    else:
        return json.dumps({"success" : res[0], "message" : res[1]})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
