import mysql.connector
import json
from datetime import datetime
import logging
class LocationDao:
 
    def __init__(self):
        logging.basicConfig(filename='locationDao.log', level=logging.DEBUG)
        self.mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="temp",
            buffered=True) 

    def reconnectSql(self):
        try:
            self.mydb.shutdown()
        except:
            logging.error("Error closing connection: Already disconnected")
            
        self.mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="temp",
            buffered=True)

    #Adds Location with attributes: qrcode of location, description of location, last pickup date at location
    def insertLocation(self, locDict):  
        try:
            logging.info("Entering insertLocation")
            val = []
            val.append(locDict['qrcode'])
            val.append(locDict['description'])
            val.append(locDict['lastPickup'])
            mycursor = self.mydb.cursor()
            sql = "INSERT INTO location (qrcode, description, lastPickup) VALUES (%s,%s,%s)"
            mycursor.execute(sql,val)
            temp = mycursor.rowcount
            logging.info("Location inserted.")
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            logging.info("insertLocation successful")
            return True, ""
        except Exception as e:
            logging.error("Error in insertLocation")
            logging.error(str(e))
            return self.handleError(e, mycursor)
    
    #Select Location based on qrcode
    def selectLocation(self,locDict):
        try: 
            logging.info("Entering selectLocation")
            qrcode=locDict['qrcode']
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT * FROM location WHERE qrcode = '" + qrcode + "'")
            myresult = mycursor.fetchall()
            # close cursor 
            mycursor.close()
            logging.info("selectLocation successful")
            return True, {"qrcode" : myresult[0][0]}
        except Exception as e:
            logging.error("Error in selectLocation")
            logging.error(str(e))
            return self.handleError(e, mycursor)
            
    def handleError(self,error, cursor=None):
        if cursor is not None:
            cursor.close()
        error = str(error)
        if "Duplicate entry" in error:
            return False,"Duplicate Entry"
        if "Can't connect to MySQL server" in error:
            self.reconnectSql()
            return False, "Could not connect to database please try again"
        if "list index out of range" in error:
            return False, "Entry could not be found"