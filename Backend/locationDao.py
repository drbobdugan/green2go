import mysql.connector
import json
from datetime import datetime
import logging
from dao import dao
class LocationDao(dao):
 
    #Adds Location with attributes: qrcode of location, description of location, last pickup date at location
    def insertLocation(self, locDict): 
        try:
            logging.info("Entering insertLocation")
            val = []
            val.append(locDict['qrcode'])
            val.append(locDict['description'])
            val.append(locDict['lastPickup'])
            sql = "INSERT INTO location (qrcode, description, lastPickup) VALUES (%s,%s,%s)"
            myresult = self.handleSQL(sql,False,val)
            if(myresult[0] == False):
                return myresult
            logging.info("insertLocation successful")
            return True, ""
        except Exception as e:
            logging.error("Error in insertLocation")
            logging.error(str(e))
            self.handleError(e)
    
    #Select Location based on qrcode
    def selectLocation(self,locDict):
        try: 
            logging.info("Entering selectLocation")
            qrcode=locDict['qrcode']
            sql = "SELECT * FROM location WHERE qrcode = '" + qrcode + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            print("I made it here")
            myresult = myresult[1][0]
            print(myresult)
            locDict={
                "qrcode": myresult[0],
                "description": myresult[1],
                "lastPickup": myresult[2]}
            print(locDict)
            logging.info("selectLocation successful")
            print("I made it here 2")
            return True, locDict
        except Exception as e:
            logging.error("Error in selectLocation")
            logging.error(str(e))
            self.handleError(e)

    #Delete Location based on qrcode
    def deleteLocation(self,locDict):
        qrcode=locDict['qrcode']
        if(self.selectLocation(locDict)[0] == False):
            return False, "Location does not exist"
        try:
            logging.info("Entering deleteLocation")
            sql = "DELETE FROM location WHERE qrcode like '" + qrcode + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("deleteLocation successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteLocation")
            logging.error(str(e))
            self.handleError(e)