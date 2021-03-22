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
        self.validCodes = self.helperHandler.extractQRCodesFromFile()
        self.validLocations = self.helperHandler.getValidLocationCodes()

    def validateQRCode(self, dic):
        # make sure valid qrcode
        if dic['qrcode'] not in self.validCodes:
            raise Exception('That is not a valid QR code.')

    def validateLocation(self, location):
        if location not in self.validLocations:
            raise Exception('That is not a valid Location.')

    def addContainer(self, request, containerDao):
        return self.containerCRUDS(request, containerDao, "addContainer")
  
    def getContainer(self, request, containerDao):
        return self.containerCRUDS(request, containerDao, "getContainer")

    def deleteContainer(self, request, containerDao):
        return self.containerCRUDS(request, containerDao, "deleteContainer")

    def updateContainer(self, request, containerDao):
        return self.containerCRUDS(request, containerDao, "updateContainer")
    
    #function values 0->add 1->get 2->delete
    def containerCRUDS(self, request, containerDao, function):
        containerDic = None
        keys = ["qrcode","auth_token", "email"]
        try:
            if function == ("getContainer" or "updateContainer"):
                containerDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t = "args", hasAuth=True)
            else:
                containerDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
            if function == "addContainer":
                self.validateQRCode(containerDic)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        function = "containerDao." + function + "(containerDic)"
        res=eval(function)
        return self.helperHandler.handleResponse(res)

    #Accepts list val in format  val = (email, qrcode, status, statusUpdateTime)
    def checkoutContainer(self, request, containerDao):
        userContainer = None
        keys=['email','qrcode','status','auth_token','location_qrcode'] # ask the database team if they are check for pendings that will switch to returned for older user
        try:
            userContainer = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
            self.validateQRCode(userContainer)
        except Exception as e:
            print(str(e))
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.addRelationship(userContainer)
        return self.helperHandler.handleResponse(res)

    def getContainersForUser(self, request, containerDao, isSorted):
        relationship = None
        keys=['email','auth_token']
        try:
            relationship = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.selectAllByEmail(relationship)
        res[1].reverse()
        if res[0] is True and isSorted is True:
            sortDict={
                'All' : res[1],
                'Checked_out':[],
                'Pending_Return':[],
                'Verified_Return':[]
            }
            for item in res[1]:
                sortDict[item['status'].replace(' ', '_')].append(item)
            res= (True,sortDict)
        return self.helperHandler.handleResponse(res)

    def checkinContainer(self, request, containerDao):  # we are going to do loction than the container so get loction for the front end here
        dictOfUserAttrib = None
        keys = ['email', 'qrcode', 'status','auth_token','location_qrcode']
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request, keys)
            self.validateQRCode(dictOfUserAttrib)
            self.validateLocation(dictOfUserAttrib['location_qrcode'])
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = containerDao.updateRelationship(dictOfUserAttrib)
        return self.helperHandler.handleResponse(res)