from flask import Flask
import mysql.connector
import json
import string
import random
from flask import request
from userDao import UserDao
from containerDao import ContainerDao
from hasContainerDao import HasContainerDao
from datetime import datetime
import sys
import os
sys.path.insert(0, os.getcwd()+'/Email/')
from emailServer import EmailManager
app = Flask(__name__)
dao=UserDao()
dao2=ContainerDao()
dao3=HasContainerDao()
emailServer = EmailManager()

#----------------------------Email Methods --------------------------------
def sendEmail(email, code):
    global emailServer
    return emailServer.sendEmail(email, code)
    

#----------------------------User Methods --------------------------------
# this crates the unique code for the user 
def id_generator(size=12, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/getUser', methods=['GET'])
def getUser():
    email = None
    try:
        email = request.args.get('email')
        if email is None:
            raise Exception("email")
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao

    res=None

    try:
        res = dao.getUser(email)
    except:
        res = {"response" : "Email does not correspond to user"}
    return res

@app.route('/addUser', methods=['POST'])
def addUser():
    newUser=None
    authCode = id_generator()
    try:
        newUser=[request.json['email'], request.json['password'], request.json['firstName'],request.json['lastName'], request.json['middleName'], request.json['phoneNum'], request.json['role'], request.json['classYear'], authCode]
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao
    res = dao.addUser(newUser)
    if res is True:
        # send email
        sendEmail(request.json['email'], authCode)
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})


@app.route('/updateUser', methods=['PATCH'])
def updateUser():
    mockuser = None
    keys = ['email', 'password', 'firstName', 'lastName', 'middleName', 'phoneNum', 'role', 'classYear', 'authCode', 'authTime', 'lastLogIn']

    dictOfUserAttrib = {key : request.json[key] if key in request.json else None for key in keys}
    global dao
    res = dao.updateUser(dictOfUserAttrib)
    if res is True:
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})

@app.route('/deleteUser', methods=['DELETE'])
def deleteUser():
    email = None
    try:
        email = request.json['email']
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao
    res = dao.deleteUser(email)
    if res is True:
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})
@app.route('/validateCode', methods=['GET'])
def validateCode():
    f='%Y-%m-%d %H:%M:%S'
    code = None
    email=None
    try:
        email = request.json['email']
        code = request.json['authcode']
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao

    res=None

    try:
        res = dao.getUser(email)

    except:
        res = {"response" : "Email does not correspond to user"}
    codefromtable=res["authCode"]
    authtime=res["authtime"]
    authtimets=datetime.strptime(authtime, f)
    timepassed=datetime.now()-authtimets
    if (code==codefromtable and timepassed.total_seconds()<300):
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})

@app.route('/login', methods=['POST'])
def login():
    email = None
    pas = None
    try:
        email = request.json["email"]
        pas = request.json["password"]
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao

    res=None

    try:
        res = dao.getUser(email)
    except:
        return {"response" : "Denied!"}
    if "password" in res and pas == res["password"]:
        return {"response" : "Success!"}
    else:
        return {"response" : "Denied!"}



#----------------------------Container Methods --------------------------------

#currently wrap the container qrcode in list because that's how db handles is in  DAO
@app.route('/addContainer', methods=['POST'])
def addContainer():
    newContainer = None
    try:
        newContainer = request.json['qrcode']
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missingfrom request"})
    global dao2
    res = dao2.addContainer([newContainer])
    if res is True:
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})

@app.route('/getContainer', methods = ['GET'])
def getContainer():
    qrcode = None
    try:
        qrcode = request.args.get('qrcode')
        if qrcode is None:
            raise Exception("qrcode")
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao2
    res = None
    try:
        res = dao2.getContainer(qrcode)
    except:
        res = {"response" : "Qr Code does not correspond to Container"}
    return res

@app.route('/deleteContainer', methods = ['DELETE'])
def deleteContainer():
    qrcode = None
    try:
        qrcode = request.json['qrcode']
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao2
    res = dao2.deleteContainer(qrcode)
    if res is True:
        return json.dumps({"response" : "Success"})
    else:
        return json.sumps({"response" : "Failed"})


@app.route('/updateContainer', methods=['PATCH'])
def updateContainer():
    mockuser = None
    keys = ['qrcode']
    dictOfContainerAttrib = {key : request.json[key] if key in request.json else None for key in keys}
    global dao2
    res = dao2.updateContainer(dictOfContainerAttrib)
    if res is True:
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})

#----------------------------HasContainer Methods --------------------------------

#Accepts list val in format  val = (email, qrcode, status, statusUpdateTime)
@app.route('/addRelationship', methods=['POST'])
def addRelationship():
    userContainer = None
    try:
        userContainer =[request.json['email'],request.json['qrcode'],request.json['status'],request.json['statusUpdateTime']]
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missingfrom request"})
    global dao3
    res = dao3.addRelationship([userContainer])
    if res is True:
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})
@app.route('/getRelationship', methods = ['GET'])
def getRelationship():
    email = None
    try:
        email = request.args.get('email')
        if email is None:
            raise Exception("email")
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao3
    res = None
    try:
        res = dao3.getRelationship(email)
    except:
        res = {"response" : "Qr Code does not correspond to Container"}
    return res

@app.route('/updateRelationship', methods=['PATCH'])
def updateRelationship():
    mockuser = None
    keys = ['email', 'qrcode', 'status', 'statusUpdateTime']

    dictOfUserAttrib = {key : request.json[key] if key in request.json else None for key in keys}
    global dao3
    res = dao3.updateRelationship(dictOfUserAttrib)
    if res is True:
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})

@app.route('/deleteRelationship', methods=['DELETE'])
def deleteRelationship():
    email = None
    try:
        email = request.json['email']
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao3
    res = dao3.deleteRelationship(email)
    if res is True:
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')