import logging
import mysql.connector
import json
from datetime import datetime
from DAO import dao
from location import Location

class LocationDao(dao):

    def selectAll(self): #returns --> "true, list of location objects"
        try:
            logging.info("Entering selectAll")
            sql = "SELECT * FROM location"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0]==False):
                return myresult
            result = []
            for row in myresult[1]:
                location = Location(row[0],row[1],row[2])
                result.append(location)
            return True, result
        except Exception as e:
            logging.error("Error in selectAll")
            logging.error(str(e))
            return self.handleError(e)
        
    def selectByLocationQRcode(self,qrcode): #returns --> "true, specific location object"
        try:
            logging.info("Entering selectByLocationQRcode")
            sql = "SELECT * FROM location WHERE location_qrcode = '" + qrcode + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0]==False):
                return myresult 
            myresult2 = myresult[1][0] #myresult looks like (true,[(qrcode,des,lastpickup)])
            location = Location(myresult2[0],myresult2[1],myresult2[2])
            return True, location
        except Exception as e:
            logging.error("Error in selectByLocationQRcode")
            logging.error(str(e))
            return self.handleError(e)

    def insertLocation(self,location):
        try:
            logging.info("Entering insertLocation")
            result = location.toLocationList()
            sql = "INSERT INTO location (location_qrcode, description, lastPickup) VALUES (%s,%s,%s)"
            myresult = self.handleSQL(sql,False,result)
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
            myresult = self.selectByLocationQRcode(location.location_qrcode)
            if(myresult[0]==False):
                return myresult
            logging.info("Entering deleteLocation")
            sql = "DELETE FROM location WHERE location_qrcode = '" + location.getQRcode() + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("deleteLocation successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteLocation")
            logging.error(str(e))
            return self.handleError(e)