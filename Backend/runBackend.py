from flask import Flask
import mysql.connector
import json
import string
import random
from flask import request
import sys
import os
sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from userDAO import UserDAO
from containerDAO import ContainerDAO
from authDAO import AuthDao
from locationDAO import LocationDao
from relationshipDAO import RelationshipDAO
from datetime import datetime
import re
import logging
from flask_cors import CORS
from pusher_push_notifications import PushNotifications
sys.path.insert(0, os.getcwd()+'/Email/')
sys.path.insert(0, os.getcwd()+'/handlers/')
sys.path.insert(0, os.getcwd()+'/Notifications/')
from notificationHelper import NotificationHelper
from emailServer import EmailManager
from authHandler import AuthHandler
from helperHandler import HelperHandler
from userHandler import UserHandler
from containerHandler import ContainerHandler
from locationHandler import LocationHandler

#app methods
app = Flask(__name__)
CORS(app)
logging.basicConfig(filename='demo.log', level=logging.DEBUG)
app.debug = True

#daos and objects
userDao=UserDAO()
containerDao=ContainerDAO()
authDao = AuthDao()
locationDao=LocationDao()
relationshipDao = RelationshipDAO()
emailServer = EmailManager()
notificationHelper = NotificationHelper()

#handlers
helperHandler = HelperHandler(emailServer)
authHandler = AuthHandler(helperHandler)
userHandler = UserHandler(helperHandler)
containerHandler = ContainerHandler(helperHandler, notificationHelper)
locationHandler = LocationHandler(helperHandler)

#----------------------------User Methods --------------------------------
@app.route('/getUser', methods=['GET'])
def getUser():
    return userHandler.getUser(request, userDao, True)

@app.route('/addUser', methods=['POST'])
def addUser():
    return userHandler.addUser(request, userDao)

@app.route('/updateUser', methods=['PATCH'])
def updateUser():
    return userHandler.updateUser(request, userDao)

@app.route('/deleteUser', methods=['DELETE'])
def deleteUser():
    return userHandler.deleteUser(request, userDao, True)

@app.route('/changePassword', methods=['PATCH'])
def changePassword():
    return userHandler.changePassword(request, userDao)

@app.route('/forgetPassword', methods=['PATCH'])
def forgetPassword():
    res=authHandler.validateCode(request,userDao,authDao)
    print(type(res))
    if "true" in str (res):
        print("here")
        return userHandler.changePassword(request, userDao)
    else: 
        return res

#----------------------------Container Methods --------------------------------
@app.route('/addContainer', methods=['POST'])
def addContainer():
    return containerHandler.addContainer(request, containerDao)

@app.route('/getContainer', methods = ['GET'])
def getContainer():
    return containerHandler.getContainer(request, containerDao)

@app.route('/deleteContainer', methods = ['DELETE'])
def deleteContainer():
    return containerHandler.deleteContainer(request, containerDao)

@app.route('/updateContainer', methods=['PATCH'])
def updateContainer():
    return containerHandler.updateContainer(request, containerDao)

@app.route('/checkoutContainer', methods=['POST'])
def checkoutContainer():
    return containerHandler.addRelationship(request, containerDao, relationshipDao)

@app.route('/getContainersForUser', methods = ['GET'])
def getContainersForUser():
    return containerHandler.getContainersForUser(request, containerDao, False)

@app.route('/getSortedContainers', methods = ['GET'])
def getSortedContainers():
    return containerHandler.getContainersForUser(request, containerDao, True)

@app.route('/checkinContainer', methods=['POST'])
def checkinContainer():
    return containerHandler.updateRelationship(request, relationshipDao)

@app.route('/reportContainer', methods=['POST'])
def reportContainer():
    return containerHandler.updateRelationship(request, relationshipDao)

@app.route('/undoReportContainer', methods=['POST'])
def undoReportContainer():
    return containerHandler.updateRelationship(request, relationshipDao)

@app.route('/getallContainers', methods=['GET'])
def getallContainers():
    return containerHandler.GetRelationships(request,relationshipDao,True)

@app.route("/getCounts",methods =['GET'])
def getCounts():
    return containerHandler.GetRelationships(request,relationshipDao,True)
#----------------------------Auth Methods --------------------------------
@app.route('/validateCode', methods=['POST'])
def validateCode():
    return authHandler.validateCode(request, userDao, authDao)

@app.route('/login', methods=['POST'])
def login():
    return authHandler.login(request, userDao, authDao)

@app.route('/auth/refresh', methods=['POST'])
def refreshCode():
    return authHandler.refreshCode(request, authDao)

@app.route('/resendAuthCode',methods=['POST'])
def resendAuthCode():
    return authHandler.resendAuthCode(request, userDao, authDao)

@app.route('/pusher/beams-auth', methods=['GET', 'OPTIONS'])
def beams_auth():
    if request.method == 'OPTIONS':
        return "true"
    val = request.args.get('id')
    return authHandler.beams_auth(val)

#----------------------------Location Methods --------------------------------
@app.route('/selectLocation',methods=['POST'])
def selectLocation():
    return locationHandler.locationcheckandAuth(request, locationDao)

@app.route('/clearLocation',methods=['PATCH'])
def clearLocation():
    return locationHandler.locationcheckandAuth(request,locationDao)

@app.route('/addLocation',methods=['POST'])
def addLocation():
    return locationHandler.addLocation(request,locationDao)

@app.route('/deleteLocation',methods=['DELETE'])
def deleteLocation():
    return locationHandler.locationcheckandAuth(request,locationDao)

@app.route('/locationList',methods=['GET'])
def locationList():
    return locationHandler.allLocations(request,locationDao)

@app.route('/updateLocation',methods=['PATCH'])
def updateLocation():
    return locationHandler.updateLocation(request,locationDao)

#----------------------------Secret Methods --------------------------------

@app.route('/secretDeleteUser', methods=['DELETE'])
def secretDeleteUser():
    return userHandler.deleteUser(request, userDao, False)

@app.route('/secretGetUser', methods=['GET'])
def secretGetUser():
    return userHandler.getUser(request, userDao, False)

@app.route('/secretDeleteRelationship', methods=['DELETE'])
def secretDeleteRelationship():
    return containerHandler.deleteRelationship(request, relationshipDao, False)

@app.route('/secretAddUser', methods=['POST'])
def secretAddUser():
    return userHandler.addUser(request, userDao)

@app.route('/secretCheckout', methods=['POST'])
def secretCheckout():
    return containerHandler.addRelationship(request, containerDao, relationshipDao)

@app.route('/secretGetRelationships', methods = ['GET'])
def secretGetRelationships():
    return containerHandler.getContainersForUser(request, containerDao, False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

