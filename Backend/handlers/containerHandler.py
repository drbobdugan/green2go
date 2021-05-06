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
from userDAO import UserDAO
from user import User
class ContainerHandler:

    def __init__(self, helperHandler, notificationHelper):
        self.helperHandler = helperHandler
        self.validCodes = self.helperHandler.extractQRCodesFromFile()
        self.validLocations = self.helperHandler.getValidLocationCodes()
        self.userDao = UserDAO()
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
        except Exception as e:
            raise Exception(e)
        return userContainer

    def secretCheckout(self, userContainer):
        try:
            userContainer['status'] = "Pending Return"
            res = self.relationdao.selectAllByStatus(userContainer['email'], userContainer['status'])
            self.helperHandler.falseQueryCheck(res)
            rel = (res[1][len(res[1])-1]) # retrieves the most recent pending return
            userContainer = rel.relationshipToDict()
            userContainer['status'] = "Checked Out"
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
        if old_code[0] is True:
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
        try:
            relationship = self.helperHandler.handleRequestAndAuth(request=request, keys=keys, t="args", hasAuth=hasAuth)
            res = self.relationdao.selectAllByEmail(relationship['email'])
            self.helperHandler.falseQueryCheck(res)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        #print(res)
        res[1].reverse()
        dictList = []
        for item in res[1]:
            item = item.relationshipToDict()
            dictList.append(item)
        res = (True, dictList)
        if isSorted is True:
            sortDict={
                'All' : dictList,
                'Checked_Out':[],
                'Pending_Return':[],
                'Verified_Return':[],
                'Damaged_Lost':[]
            }
            for item in dictList:
                #print(item['status'].replace(' ', '_'))
                sortDict[item['status'].replace(' ', '_')].append(item)
            res = (True,sortDict)
        return self.helperHandler.handleResponse(res)
    
    def reportContainer(self, userContainer):
        try:
            userContainer['location_qrcode'] = None
        except Exception as e:
            raise Exception(e)
        return userContainer

    def checkinContainer(self, userContainer):
        try:
            self.validateQRCode(userContainer['location_qrcode'], True)
            userContainer['statusUpdateTime']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            raise Exception(e)
        return userContainer
    
    def undoReport(self, userContainer):
        try:
            userContainer['status'] = 'Checked Out'
            userContainer['description'] = None
        except Exception as e:
            raise Exception(e)
        return userContainer

    def updateRelationship(self, request, containerDao):  # we are going to do loction than the container so get loction for the front end here
        userContainer = None
        if "/checkinContainer" in str(request):
            keys = ['email', 'qrcode', 'status','auth_token','location_qrcode']
            func = "self.checkinContainer(userContainer)"
        elif "/reportContainer" in str(request):
            keys = ['email', 'qrcode', 'status', 'auth_token', 'description']
            func = "self.reportContainer(userContainer)"
        elif "/undoReportContainer" in str(request):
            keys = ['email', 'qrcode', 'auth_token']
            func = "self.undoReport(userContainer)"
        try:
            userContainer = self.helperHandler.handleRequestAndAuth(request, keys)
            userContainer = eval(func)
            self.validateQRCode(userContainer['qrcode'], False)
            rel = self.relationdao.selectActiveQRcode(userContainer["qrcode"])
            if "/checkinContainer" in str(request):
                reward = self.addPoints(rel[1][0])
            self.helperHandler.falseQueryCheck(rel)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        #print(dictOfUserAttrib)
        #change over to search by qrcode and active = 1
        relationship = rel[1][0]
        relDict = relationship.relationshipToDict()
        if "/undoReportContainer" in str(request) and relDict['status'] != "Damaged Lost":
            return json.dumps({"success" : False, "message" : "Container is not Damaged Lost"})
        for key in userContainer:
            if key != "auth_token" and key != "email":
                relDict[key] = userContainer[key]
        relationship.dictToRelationship(relDict)
        res = self.relationdao.updateRelationship(relationship)
        if "/checkinContainer" in str(request):
            res = reward
        return self.helperHandler.handleResponse(res)

    def addPoints(self, rel):
        try:
            f='%Y-%m-%d %H:%M:%S'
            relDict = rel.relationshipToDict()
            res = self.userDao.selectUser(relDict['email'])
            self.helperHandler.falseQueryCheck(res)
            user = res[1]
            userDict = user.userToDict()
            points = userDict['points']
            checkoutTime = str(relDict['statusUpdateTime'])
            authtimets=datetime.strptime(checkoutTime, f)
            timepassed=datetime.now()-authtimets
            if (timepassed.total_seconds() / 3600) >= 48 and relDict['status'] == "Checked Out":
                points = points + 5
                userDict['points'] = points
                reward = self.rewardCheck(15, userDict)
            elif (timepassed.total_seconds() / 3600) < 48 and relDict['status'] == "Checked Out":
                points = points + 15
                userDict['points'] = points
                reward = self.rewardCheck(15, userDict)
            else:
                reward = ""
            user.dictToUser(userDict)
            res = self.userDao.updateUser(user)
            self.helperHandler.falseQueryCheck(res)
        except Exception as e:
            raise Exception(e)
        return (True, reward)

    def rewardCheck(self, newPoints, userDic):
        if userDic['points'] // 300 > 0 and userDic['points'] % 300 < newPoints:
            userDic['reward_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return {'newReward' : 'True', 'points' : newPoints}
        else:
            return {'newReward' : 'False', 'points' : newPoints}

    def deleteRelationship(self, request, relationshipDao, hasAuth):
        relDict = None
        #auth_token not required for testing
        keys = ['email', 'qrcode']
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
            relDict = []
            for item in rel[1]:
                relDict.append(item.relationshipToDict())
            rel = (True, relDict)
        elif '/getCounts' in str(request):
            sitedic={"In Stock":self.containerdao.totalContainersInStock()[1],"Checked Out":self.containerdao.totalContainersCheckedOut()[1],"In Bin":self.containerdao.totalContainersInBins()[1],"Damaged Lost":self.containerdao.totalContainersDamagedLost()[1]}
            rel=[True,sitedic]
            if rel[0] is False:
                return self.helperHandler.handleResponse(rel)
        elif '/getCurrent' in str(request):
            rel=self.containerdao.selectRecentStatus()
            if rel[0] is False:
                return self.helperHandler.handleResponse(rel)
        
        return self.helperHandler.handleResponse(rel)      
