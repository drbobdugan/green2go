import json
import string
import sys
import os
from datetime import datetime
sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from locationDAO import LocationDao
from location import Location
# test
class LocationHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler
        self.locationdao = LocationDao()

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


    def selectLocation(self, request,locationDao,res):
        res=res[0],res[1].locationToDict()
        return self.helperHandler.handleResponse(res)
        
    def clearlocation(self,request,locationDao,res):
        res[1].lastPickup=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res2=self.locationdao.updateLocation(res[1])

        return self.helperHandler.handleResponse(res2)
