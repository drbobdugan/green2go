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
        self.locationdao= LocationDao()
        self.notificationHelper = notificationHelper

    def validateQRCode(self, qrcode, isLocation):
        # make sure valid qrcode
        if isLocation == False:
            res = self.containerdao.selectContainer(qrcode)
        elif isLocation == True:
            res = self.locationdao.selectByLocationQRcode(qrcode)
        if res[0] == False and isLocation == False:
            raise Exception('That is not a valid QR code.')
        elif res[0] == False and isLocation == True:
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
        t = "json"
        keys = ["qrcode","auth_token", "email"]
        if function == ("selectContainer" or "updateContainer"):
            t = "args"
        try:
            containerDic = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t = t, hasAuth=True)
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

    def checkoutContainer(self, userContainer):
        try:
            self.validateQRCode(userContainer['qrcode'], False)
            userContainer['description'] = None
            userContainer['active'] = "1"
        except Exception as e:
            raise Exception(e)
        return userContainer

    def reportContainer(self, userContainer):
        try:
            userContainer['location_qrcode'] = None
            userContainer['active'] = "1"
            self.validateQRCode(userContainer['qrcode'], False)
        except Exception as e:
            raise Exception(e)
        return userContainer

    def secretCheckout(self, userContainer):
        try:
            userContainer['status'] = "Pending Return"
            res = self.relationdao.selectAllByStatus(userContainer['email'], userContainer['status'])
            self.helperHandler.falseQueryCheck(res)
            userContainer = (res[1][len(res[1])-1]) # retrieves the most recent pending return
            userContainer['status'] = "Checked Out"
            userContainer['active'] = "1"
            userContainer['email'] = "Checkout@stonehill.edu"
        except Exception as e:
            raise Exception(e) 
        return userContainer


    #Accepts list val in format  val = (email, qrcode, status, statusUpdateTime)
    def addRelationship(self, request, containerDao, relationshipDAO):
        userContainer = None
        hasAuth = True
        if "/checkoutContainer" in str(request):
            keys = ['email', 'qrcode', 'status', 'auth_token', 'location_qrcode']
            func = "self.checkoutContainer(userContainer)" # ask the database team if they are check for pendings that will switch to returned for older user
        elif "/reportContainer" in str(request):
            keys = ['email', 'qrcode', 'status', 'auth_token', 'description']
            func = "self.reportContainer(userContainer)"
        elif "/secretCheckout" in str(request):
            keys = ['email']
            func = "self.secretCheckout(userContainer)"
            hasAuth = False
        try:
            userContainer = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, hasAuth=hasAuth)
            userContainer = eval(func)
            userContainer['statusUpdateTime']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            old_code = relationshipDAO.getRecentUser(userContainer['qrcode'])
            relationship=Relationship()
            relationship.dictToRelationship(userContainer)
            res = self.relationdao.insertRelationship(relationship)
            self.helperHandler.falseQueryCheck(res)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        # send notification
        if old_code[0] is True and "/reportContainer" not in str(request):
            self.notificationHelper.sendNotification(old_code[1])
        return self.helperHandler.handleResponse(res)

    def getContainersForUser(self, request, containerDao, isSorted):
        relationship = None
        if "/secretGetRelationships" in str(request):
            keys=['email']
            hasAuth = False
        else:
            keys=['email', 'auth_token']
            hasAuth = True
        print("abc")
        try:
            relationship = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=hasAuth)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = self.relationdao.selectAllByEmail(relationship['email'])
        #print(res)
        
        res[1].reverse()
        damagedQR = []
        for item in res[1]:
            if item['status'] == "Damaged Lost":
                damagedQR.append(item['qrcode'])
            if item['qrcode'] in damagedQR and item['status'] == "Checked Out":
                res[1].remove(item)
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
            self.validateQRCode(dictOfUserAttrib['qrcode'], False)
            self.validateQRCode(dictOfUserAttrib['location_qrcode'], True)
            dictOfUserAttrib['statusUpdateTime']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            rel = self.relationdao.selectActiveQRcode(dictOfUserAttrib["qrcode"])
            self.helperHandler.falseQueryCheck(rel)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        #print(dictOfUserAttrib)
        #change over to search by qrcode and active = 1
        relationship = Relationship()
        relationship.listToRelationship(rel[1][0])
        relDict = relationship.relationshipToDict()
        for key in dictOfUserAttrib:
            if key != "auth_token" and key != "email":
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
            self.validateQRCode(relDict['qrcode'], False)
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

    def GetRelationships(self,request,relationshipDao,hasAuth):
        relDict = None
        keys=['email','auth_token']
        try:
            relDict = self.helperHandler.handleRequestAndAuth(request, keys, t="args", hasAuth=True )
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        if '/getallContainers' in str(request):
            rel=self.relationdao.selectAll()
            if rel[0] is False:
                return self.helperHandler.handleResponse(rel)
        elif '/getCounts' in str(request):
            sitedic={"In Stock":self.containerdao.totalContainersInStock()[1],"Checked Out":self.containerdao.totalContainersCheckedOut()[1],"In Bin":self.containerdao.totalContainersInBins()[1],"Pending Returns":self.relationdao.selectPendingReturns()[1]}
            rel=[True,sitedic]
            if rel[0] is False:
                return self.helperHandler.handleResponse(rel)
        return self.helperHandler.handleResponse(rel)      
