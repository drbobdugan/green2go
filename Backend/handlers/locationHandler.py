import json
import string
from datetime import datetime
from userDao import UserDao
from containerDao import ContainerDao
from authDao import AuthDao
from locationDao import LocationDao
# test
class LocationHandler:

    def __init__(self, helperHandler):
        self.helperHandler = helperHandler


    def selectLocation(self, request,locationDao):
        locationDic = None
        keys = ["qrcode",'email','auth_token']
        try:
            locationDic = self.helperHandler.handleRequestAndAuth(request, keys)
        except Exception as e:
            return json.dumps({"success" : False, "message" : str(e)})
        res = locationDao.selectLocation(locationDic)  #need to get the method for database team 
        return self.helperHandler.handleResponse(res)