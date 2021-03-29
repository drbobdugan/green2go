import json
import string
import os
import sys
from datetime import datetime
from userDao import UserDao

sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from containerDAO import ContainerDAO
from authDao import AuthDao
from locationDao import LocationDao
from relationshipDAO import RelationshipDAO
from relationship import Relationship
from container import Container
class ContainerHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler
        self.validCodes = self.helperHandler.extractQRCodesFromFile()
        self.validLocations = self.helperHandler.getValidLocationCodes()
        self.relationdao = RelationshipDAO()
        self.containerdao = ContainerDAO()

    def validateQRCode(self, dic):
        # make sure valid qrcode
        if dic['qrcode'] not in self.validCodes:
            raise Exception('That is not a valid QR code.')

    def validateLocation(self, location):
        if location not in self.validLocations:
            raise Exception('That is not a valid Location.')

    def addContainer(self, request, containerDao):
        return self.containerCRUDS(request, containerDao, "insertContainer")
  
    def getContainer(self, request, containerDao):
        return self.containerCRUDS(request, containerDao, "selectContainer")

    def deleteContainer(self, request, containerDao):
        return self.containerCRUDS(request, containerDao, "deleteContainer")

    def updateContainer(self, request, containerDao):
        return self.containerCRUDS(request, containerDao, "updateContainer")
    
    #function values 0->add 1->get 2->delete
    def containerCRUDS(self, request, containerDao, function):
        containerDic = None
        keys = ["qrcode","auth_token", "email"]
        try:
            if function == ("selectContainer" or "updateContainer"):
                containerDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t = "args", hasAuth=True)
            else:
                containerDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
            if function == "insertContainer":
                self.validateQRCode(containerDic)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        container=Container()
        container.dictToContainer(containerDic)
        if(function == "selectContainer"):
            function = "self.containerdao." + function + "(containerDic['qrcode'])"
            
        else:
            function = "self.containerdao." + function + "(container)"
        res=eval(function)
        if (type(res[1])==type(container)):
            res= res[0],res[1].containerToDict()
        return self.helperHandler.handleResponse(res)

    #Accepts list val in format  val = (email, qrcode, status, statusUpdateTime)
    def checkoutContainer(self, request, containerDao):
        userContainer = None
        keys=['email','qrcode','status','auth_token','location_qrcode'] # ask the database team if they are check for pendings that will switch to returned for older user
        try:
            userContainer = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=True)
            self.validateQRCode(userContainer)
            userContainer['statusUpdateTime']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            #print(str(e))
            return json.dumps({"success" : False, "message" : str(e)})
        relationship=Relationship()
        
        relationship.dictToRelationship(userContainer)
        
        res = self.relationdao.insertRelationship(relationship)
        return self.helperHandler.handleResponse(res)

    def getContainersForUser(self, request, containerDao, isSorted):
        relationship = None
        keys=['email','auth_token']
        try:
            relationship = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=True)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = self.relationdao.selectAllByEmail(relationship['email'])
        #print(res)
        
        res[1].reverse()
        if res[0] is True and isSorted is True:
            sortDict={
                'All' : res[1],
                'Checked_out':[],
                'Pending_Return':[],
                'Verified_Return':[]
            }
            for item in res[1]:
                #print(item['status'].replace(' ', '_'))
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
            dictOfUserAttrib['statusUpdateTime']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        relationship=Relationship()
        #print(dictOfUserAttrib)
        relationship.dictToRelationship(dictOfUserAttrib)
        res = self.relationdao.updateRelationship(relationship)
        return self.helperHandler.handleResponse(res)