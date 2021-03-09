import json
import string
from datetime import datetime
from userDao import UserDao
from containerDao import ContainerDao
from authDao import AuthDao
from locationDao import LocationDao

class ContainerHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler

    def addContainer(self, request, containerDao):
        containerDic = None
        keys = ["qrcode"]
        try:
            containerDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.addContainer(containerDic)
        return self.helperHandler.handleResponse(res)
  
    def getContainer(self, request, containerDao):
        containerDic = None
        keys = ["qrcode", "auth_token", "email"]
        try:
            containerDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.getContainer(containerDic)
        return self.helperHandler.handleResponse(res)

    def deleteContainer(self, request, containerDao):
        containerDic = None
        keys = ["qrcode", "auth_token", "email"]
        try:
            containerDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.deleteContainer(containerDic)
        return self.helperHandler.handleResponse(res)

    def updateContainer(self, request, containerDao):
        containerDic = None
        keys = ['qrcode', "auth_token", "email"]
        try:
            containerDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.updateContainer(containerDic)
        return self.helperHandler.handleResponse(res)

    #Accepts list val in format  val = (email, qrcode, status, statusUpdateTime)
    def checkoutContainer(self, request, containerDao):
        userContainer = None
        keys=['email','qrcode','status','auth_token','location_qrcode'] # ask the database team if they are check for pendings that will switch to returned for older user
        try:
            userContainer = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.addRelationship(userContainer)
        return self.helperHandler.handleResponse(res)

    def getContainersForUser(self, request, containerDao):
        relationship = None
        keys=['email','auth_token']
        try:
            relationship = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.selectAllByEmail(relationship)
        return self.helperHandler.handleResponse(res)

    def checkinContainer(self, request, containerDao):  # we are going to do loction than the container so get loction for the front end here
        dictOfUserAttrib = None
        keys = ['email', 'qrcode', 'status','auth_token','location_qrcode']
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request, keys)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.updateRelationship(dictOfUserAttrib)
        return self.helperHandler.handleResponse(res)