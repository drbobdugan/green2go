import json
import string
import os
import sys
from datetime import datetime

sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from containerDAO import ContainerDAO
from authDAO import AuthDao
from locationDAO import LocationDao
from relationshipDAO import RelationshipDAO
from relationship import Relationship
from container import Container
class ContainerHandler:

    def __init__(self, helperHandler, notificationHelper):
        self.helperHandler = helperHandler
        self.validCodes = self.helperHandler.extractQRCodesFromFile()
        self.validLocations = self.helperHandler.getValidLocationCodes()
        self.relationdao = RelationshipDAO()
        self.containerdao = ContainerDAO()
        self.notificationHelper = notificationHelper

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
    def addRelationship(self, request, containerDao, relationshipDAO):
        userContainer = None
        hasAuth = True
        if "/checkoutContainer" in str(request):
            keys=['email','qrcode','status','auth_token','location_qrcode'] # ask the database team if they are check for pendings that will switch to returned for older user
        elif "/reportContainer" in str(request):
            keys = ['email', 'qrcode', 'status', 'auth_token', 'description']
        try:
            userContainer = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=hasAuth)
            self.validateQRCode(userContainer)
            userContainer['statusUpdateTime']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if "/checkoutContainer" in str(request):
                userContainer['description'] = None
                userContainer['active'] = "1"
            elif "/reportContainer" in str(request):
                userContainer['location_qrcode'] = None
                userContainer['active'] = "0"
        except Exception as e:
            #print(str(e))
            return json.dumps({"success" : False, "message" : str(e)})

        # send notification
        old_code = relationshipDAO.getRecentUser(userContainer['qrcode'])
        if old_code[0] is True and "/checkoutContainer" in str(request):
            self.notificationHelper.sendNotification(old_code[1])

        relationship=Relationship()
        relationship.dictToRelationship(userContainer)
        print(relationship.relationshipToList())
        res = self.relationdao.insertRelationship(relationship)
        print(res)
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
                'Checked_Out':[],
                'Pending_Return':[],
                'Verified_Return':[],
                'Damaged_Lost':[]
            }
            for item in res[1]:
                #print(item['status'].replace(' ', '_'))
                sortDict[item['status'].replace(' ', '_')].append(item)
            res= (True,sortDict)
        return self.helperHandler.handleResponse(res)

    def updateRelationship(self, request, containerDao):  # we are going to do loction than the container so get loction for the front end here
        dictOfUserAttrib = None
        keys = ['email', 'qrcode', 'status','auth_token','location_qrcode']
        try:
            dictOfUserAttrib = self.helperHandler.handleRequestAndAuth(request, keys)
            self.validateQRCode(dictOfUserAttrib)
            self.validateLocation(dictOfUserAttrib['location_qrcode'])
            dictOfUserAttrib['statusUpdateTime']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        #print(dictOfUserAttrib)
        rel = self.relationdao.selectRelationship(dictOfUserAttrib["email"], dictOfUserAttrib["qrcode"])
        relationship = rel[1]
        relDict = relationship.relationshipToDict()
        for key in dictOfUserAttrib:
            if key != "auth_token":
                relDict[key] = dictOfUserAttrib[key]
        relationship.dictToRelationship(relDict)
        res = self.relationdao.updateRelationship(relationship)
        return self.helperHandler.handleResponse(res)


    def deleteRelationship(self, request, relationshipDao, hasAuth):
        relDict = None
        #auth_token not required for testing
        keys = ['email', 'qrcode']
        if "/undoReportContainer" in str(request):
            keys.append('auth_token')
        try:
            relDict = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=hasAuth)
            self.validateQRCode(relDict)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        #get relationship object based on email and qrcode
        rel = self.relationdao.selectRelationship(relDict['email'], relDict['qrcode'])
        if rel[0] is False:
            return self.helperHandler.handleResponse(rel)
        relationship = rel[1]
        relDict = relationship.relationshipToDict()
        if "/undoReportContainer" in str(request) and relDict['status'] != "Damaged Lost":
            return json.dumps({"success" : False, "message" : "Container is not Damaged Lost"})
        #delete relationship from table
        res = self.relationdao.deleteRelationship(relationship)
        return self.helperHandler.handleResponse(res)
# to get all containers for admin

    def GetallRelationships(self,request,relationshipDao,hasAuth):
        relDict = None
        keys=['email','auth_token']
        try:
            relDict = self.helperHandler.handleRequestAndAuth(request, keys, t="args", hasAuth=True )
        except Exception as e:
    
            return json.dumps({"success" : False, "message" : str(e)})
        rel=self.relationdao.selectAll()
        if rel[0] is False:
            return self.helperHandler.handleResponse(rel)

        return self.helperHandler.handleResponse(rel)

# checkout Container Tool
    def checkoutTool(self, request, relationshipDao, hasAuth=False):
        relDict = None
        keys=['email']
        try:
            relDict = self.helperHandler.handleRequestAndAuth(request, keys, hasAuth=False)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        relDict['status'] = "Pending Return"
        res = self.relationdao.selectAllByStatus(relDict['email'], relDict['status'])
        relDict = (res[1][len(res[1])-1]) # retrieves the most recent pending return
        relDict['status'] = "Checked Out"
        relDict['statusUpdateTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        relationship = Relationship()
        relationship.dictToRelationship(relDict)
        res = self.relationdao.insertRelationship(relationship)
        print(res)
        if (res[0] is True):
            res = self.relationdao.deleteRelationship(relationship)
        print(res)

        return self.helperHandler.handleResponse(res)
        
