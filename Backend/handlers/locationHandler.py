import json
import string
import sys
import os
from datetime import datetime
sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from locationDAO import LocationDao
from location import Location
from containerDAO import ContainerDAO
from container import Container
# test
class LocationHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler
        self.locationdao = LocationDao()
        self.containerdao = ContainerDAO()

    def locationcheckandAuth(self,request,locationDao):
        locationDic = None
        keys = ["qrcode",'email','auth_token']
        try:
            locationDic = self.helperHandler.handleRequestAndAuth(request, keys)
            res = self.locationdao.selectByLocationQRcode(locationDic['qrcode'])
            self.helperHandler.falseQueryCheck(res)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        if "/selectLocation" in str (request):
            return self.selectLocation(request,locationDao,res)
        elif "/clearLocation" in str (request):
            return self.clearlocation(request,locationDao,res)
        elif "/deleteLocation" in str (request):
            return self.deleteLocation(request,locationDao,res)


    def selectLocation(self, request,locationDao,res):
        res=res[0],res[1].locationToDict()
        return self.helperHandler.handleResponse(res)
        
    def clearlocation(self,request,locationDao,res):
        res[1].lastPickup=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res2=self.locationdao.updateLocation(res[1])

        return self.helperHandler.handleResponse(res2)

    def addLocation(self,request,locationDao):
        locationDic = None
        keys = ['location_qrcode','email','auth_token','description']
        try:
            locationDic = self.helperHandler.handleRequestAndAuth(request, keys)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        locationDic['lastPickup'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        location = Location()
        location.dictToLocation(locationDic)
        res = self.locationdao.insertLocation(location)
        return self.helperHandler.handleResponse(res)
    
    def deleteLocation(self,request,locationDao,res):
        res2=self.locationdao.deleteLocation(res[1])
        return self.helperHandler.handleResponse(res2)

    def allLocations(self,request,locationDao):
        locationDic = None
        keys = ['email','auth_token']
        locations=[]
        try:
            locationDic = self.helperHandler.handleRequestAndAuth(request, keys, t="args", hasAuth=True )
            res = self.locationdao.selectAll()
            self.helperHandler.falseQueryCheck(res)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        BinCounts = self.containerdao.totalContainersInBins()[1]
        for r in res[1]:
            tempLoc = r.locationToDict()
            counter = 0
            for item in BinCounts:
                if item['location_qrcode'] == tempLoc['location_qrcode']:
                    counter = counter + 1
            tempLoc.update({'count' : counter})
            locations.append(tempLoc)
        res=res[0],locations
        return self.helperHandler.handleResponse(res)

    def updateLocation(self,request,locationDao):
        locationDic = None
        keys = ['qrcode','email','auth_token','description']
        try:
            locationDic = self.helperHandler.handleRequestAndAuth(request, keys)
            res = self.locationdao.selectByLocationQRcode(locationDic['qrcode'])
            self.helperHandler.falseQueryCheck(res)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        
        res[1].description=locationDic['description']
        res2=self.locationdao.updateLocation(res[1])
        return self.helperHandler.handleResponse(res2)







