import json
import string
import sys
import os
from datetime import datetime
from userDao import UserDao
from containerDao import ContainerDao
from authDao import AuthDao
sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from locationDAO import LocationDao
# test
class LocationHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler
        self.locationdao = LocationDao()


    def selectLocation(self, request,locationDao):
        locationDic = None
        keys = ["qrcode",'email','auth_token']
        try:
            locationDic = self.helperHandler.handleRequestAndAuth(request, keys)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
       
        print(locationDic)
        res = self.locationdao.selectByLocationQRcode(locationDic['qrcode']) #need to get the method for database team 
        res=res[0],res[1].locationToDict()
        return self.helperHandler.handleResponse(res)