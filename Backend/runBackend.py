from flask import Flask
import mysql.connector
import json
import string
import random
from flask import request
from userDao import UserDao
from containerDao import ContainerDao
from datetime import datetime
import sys
import os
import re
sys.path.insert(0, os.getcwd()+'/Email/')
from emailServer import EmailManager
app = Flask(__name__)
dao=UserDao()
dao2=ContainerDao()

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

#----------------------------Email Methods --------------------------------
def sendEmail(email, code):
    global emailServer
    return emailServer.sendEmail(email, code)

def validateEmail(email):
    if not re.match("([a-zA-Z0-9_.+-]+@+((students\.stonehill\.edu)|(stonehill\.edu))$)", email):
        return False
    return True
    

#----------------------------User Methods --------------------------------
# this crates the unique code for the user 
def id_generator(size=12, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/getUser', methods=['GET'])
def getUser():
    dictOfUserAttrib = None
    keys = ["email"]
    try:
        dictOfUserAttrib = extractKeysFromRequest(request, keys, t="args")
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao

    res=None

    try:
        res = dao.getUser(dictOfUserAttrib)
    except:
        res = {"success" : False, "message" : "Database error"}
    return res

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
    if res is True:
        # send email
        sendEmail(request.json['email'], authCode)
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Database error"})


@app.route('/updateUser', methods=['PATCH'])
def updateUser():
    mockuser = None
    keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear', 'authCode', 'authTime', 'lastLogIn']

    dictOfUserAttrib = extractKeysFromRequest(request, keys)
    global dao
    res = dao.updateUser(dictOfUserAttrib)
    if res is True:
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Database error"})

@app.route('/deleteUser', methods=['DELETE'])
def deleteUser():
    dictOfUserAttrib = None
    keys = ['email']
    try:
        dictOfUserAttrib = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao
    res = dao.deleteUser(dictOfUserAttrib)
    if res is True:
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Database error"})


        
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
    codefromtable=res["authCode"]
    authtime=res["authtime"]
    authtimets=datetime.strptime(authtime, f)
    timepassed=datetime.now()-authtimets
    if (dic['code']==codefromtable and timepassed.total_seconds()<300):
        return json.dumps({"success" : True, "message" : ""})
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

    res=None

    try:
        res = dao.getUser(dic)
    except:
        return json.dumps({"success" : False, "message" : "Database error"})
    if "password" in res and dic["password"] == res["password"]:
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Incorrect password"})



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
    if res is True:
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Database error"})

@app.route('/getContainer', methods = ['GET'])
def getContainer():
    containerDic = None
    keys = ["qrcode"]
    try:
        containerDic = extractKeysFromRequest(request, keys, t="args")
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao2
    res = None
    try:
        res = json.dumps(dao2.getContainer(containerDic))
    except:
        res = json.dumps({"success" : False, "message" : "Database error"})
    return res

@app.route('/deleteContainer', methods = ['DELETE'])
def deleteContainer():
    containerDic = None
    keys = ["qrcode"]
    try:
        containerDic = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao2
    res = dao2.deleteContainer(containerDic)
    if res is True:
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Database error"})


@app.route('/updateContainer', methods=['PATCH'])
def updateContainer():
    containerDic = None
    keys = ['qrcode']
    containerDic = extractKeysFromRequest(request, keys)
    global dao2
    res = dao2.updateContainer(containerDic)
    if res is True:
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Database error"})

#----------------------------HasContainer Methods --------------------------------

#Accepts list val in format  val = (email, qrcode, status, statusUpdateTime)
@app.route('/addRelationship', methods=['POST'])
def addRelationship():
    userContainer = None
    keys=['email','qrcode','status','statusUpdateTime']
    try:
        userContainer = extractKeysFromRequest(request, keys)
    except Exception as e:
        return json.dumps({"success" : False, "message" : str(e).replace("'", '') + " field missing from request"})
    global dao2
    res = dao2.addRelationship([userContainer])
    if res is True:
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Database error"})
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
    res = None
    try:
        res = dao2.getRelationship(relationship)
    except:
        res = json.dumps({"success" : False, "message" : "QRcode did not correspond to container"})
    return res

@app.route('/updateRelationship', methods=['PATCH'])
def updateRelationship():
    dictOfUserAttrib = None
    keys = ['email', 'qrcode', 'status', 'statusUpdateTime']

    dictOfUserAttrib = extractKeysFromRequest(request, keys)
    global dao2
    res = dao2.updateRelationship(dictOfUserAttrib)
    if res is True:
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Databse error"})

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
    if res is True:
        return json.dumps({"success" : True, "message" : ""})
    else:
        return json.dumps({"success" : False, "message" : "Database error"})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
