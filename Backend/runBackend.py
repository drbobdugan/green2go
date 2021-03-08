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
sys.path.insert(0, os.getcwd()+'/handlers/')
from emailServer import EmailManager
from authHandler import AuthHandler
from helperHandler import HelperHandler
from userHandler import UserHandler
from containerHandler import ContainerHandler
from locationHandler import LocationHandler

#app methods
app = Flask(__name__)
app.debug = True

#daos and objects
userDao=UserDao()
containerDao=ContainerDao()
authDao = AuthDao()
locationDao=LocationDao()
emailServer = EmailManager()

#handlers
helperHandler = HelperHandler(emailServer)
authHandler = AuthHandler(helperHandler)
userHandler = UserHandler(helperHandler)
containerHandler = ContainerHandler(helperHandler)
locationHandler = LocationHandler(helperHandler)

#----------------------------User Methods --------------------------------
@app.route('/getUser', methods=['GET'])
def getUser():
    return userHandler.getUser(request, userDao, containerDao)

@app.route('/addUser', methods=['POST'])
def addUser():
    return userHandler.addUser(request, userDao)

@app.route('/updateUser', methods=['PATCH'])
def updateUser():
    return userHandler.updateUser(request, userDao)

@app.route('/deleteUser', methods=['DELETE'])
def deleteUser():
    return userHandler.deleteUser(request, userDao)

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
    return containerHandler.checkoutContainer(request, containerDao)

@app.route('/getContainersForUser', methods = ['GET'])
def getContainersForUser():
    return containerHandler.getContainersForUser(request, containerDao)

@app.route('/checkinContainer', methods=['POST'])
def checkinContainer():
    return containerHandler.checkinContainer(request, containerDao)

#----------------------------Validity Methods --------------------------------
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

#----------------------------Location Methods --------------------------------
@app.route('/selectLocation',methods=['POST'])
def selectLocation():
    return locationHandler.selectLocation(request, locationDao)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
