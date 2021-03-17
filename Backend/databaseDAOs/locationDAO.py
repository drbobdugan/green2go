import logging
FORMAT = "[%(asctime)s%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
logging.basicConfig(filename='output.log',format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
import mysql.connector
import json
from datetime import datetime
from DAO import dao
from location import Location

class LocationDao(dao):

    def selectAll(self):
        sql = "SELECT * FROM location"
        myresult = self.handleSQL(sql,True,None)
        if(myresult[0]==False):
            return myresult
        result = []
        for row in myresult[1]:
            location = Location(row[0],row[1],row[2])
            result.append(location)
        return result
    
    def selectByLocationQRcode(self,qrcode):
        sql = "SELECT * FROM location WHERE location_qrcode = '" + qrcode + "'"
        myresult = self.handleSQL(sql,True,None)
        print(myresult)
        if(myresult[0]==False):
            return myresult
        myresult = myresult[1][0]
        location = Location(myresult[1][0],myresult[1][1],myresult[1][2])
        return location

    def insertLocation(self,location):
        try:
            logging.info("Entering insertLocation")
            result = location.toLocationList()
            sql = "INSERT INTO location (location_qrcode, description, lastPickup) VALUES (%s,%s,%s)"
            myresult = self.handleSQL(sql,False,result)
            #print(myresult)
            if(myresult[0] == False):
                return myresult
            logging.info("insertLocation successful")
            return True, ""
        except Exception as e:
            logging.error("Error in insertLocation")
            logging.error(str(e))
            return self.handleError(e)

    def deleteLocation(self,location):
        try:
            if(self.selectByLocationQRcode(location)[0] == False):
                return False, "Location does not exist"
            logging.info("Entering deleteLocation")
            sql = "DELETE FROM location WHERE qrcode = '" + location.getQRcode() + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("deleteLocation successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteLocation")
            logging.error(str(e))
            return self.handleError(e)