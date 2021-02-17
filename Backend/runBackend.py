from flask import Flask
import mysql.connector
import json
from flask import request
from userDao import UserDao
from containerDao import ContainerDao
app = Flask(__name__)
dao=UserDao()
dao2=ContainerDao()

#----------------------------User Methods --------------------------------

@app.route('/getUser', methods=['GET'])
def getUser():
    email = None
    try:
        email = request.json['email']
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
    try:
        newUser=[request.json['email'], request.json['password'], request.json['firstName'],request.json['lastName'], request.json['middleName'], request.json['phoneNum'], request.json['role'], request.json['classYear'], request.json['authCode'],request.json['authTime'],request.json['lastLogIn']]
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missing from request"})
    global dao
    res = dao.addUser(newUser)
    if res is True:
        return json.dumps({"response" : "Success"})
    else:
        return json.dumps({"response" : "Failed"})


@app.route('/updateUser', methods=['UPDATE'])
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


#----------------------------Container Methods --------------------------------

@app.route('/addContainer', methods=['POST'])
def addContainer():
    newContainer = None
    try:
        newContainer = request.json['qrcode']
    except Exception as e:
        return json.dumps({"error" : str(e).replace("'", '') + " field missingfrom request"})
    global dao2
    res = dao2.addContainer(newContainer)
    if res is true:
        return json.dumps({"response: Success"})
    else:
        return json.dumps({"response: Failed"})

@app.route('/getContainer', methods = ['GET'])
def getContainer():
    qrcode = None
    try:
        qrcode = request.json['qrcode']
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
    res = deleteContainer(qrcode)
    if res is true:
        return json.dumps({"response: Success"})
    else:
        return json.sumps({"response: Failed"})


@app.route('/updateContainer', methods=['UPDATE'])
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

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')