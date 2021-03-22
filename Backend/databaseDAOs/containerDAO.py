import mysql.connector
from datetime import datetime
import logging
from container import Container
from DAO import dao
class ContainerDAO(dao):

    # CREATE CONTAINER
    def insertContainer(self,c):
        try:
            logging.info("Entering insertContainer")
            result = c.toContainerList()
            sql = "INSERT INTO container (qrcode) VALUE (%s)"
            myresult = self.handleSQL(sql,False,result)
            if(myresult[0] == False):
                return myresult
            logging.info("insertContainer successful")
            return True, ""
        except Exception as e:
            logging.error("Error in insertContainer")
            logging.error(str(e))
            return self.handleError(e)
    
    # READ CONTAINER
    def selectContainer(self,qrcode):
        try: 
            logging.info("Entering selectContainer")
            sql = "SELECT * FROM container WHERE qrcode = '" + qrcode + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            logging.info("selectContainer successful")
            return True, {"qrcode" : myresult[1][0][0]}
        except Exception as e:
            logging.error("Error in selectContainer")
            logging.error(str(e))
            return self.handleError(e)

    # UPDATE CONTAINER
    #def updateContainer(self,c): #idk if we need this method but if so it will be like DELETE sql

    # DELETE CONTAINER
    def deleteContainer(self,c):
        try:
            logging.info("Entering deleteContainer")
            result = c.toContainerList()
            sql = "DELETE FROM container WHERE qrcode = '" + result[0] + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("deleteContainer successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteContainer")
            logging.error(str(e))
            return self.handleError(e)
# ____________________________________________________________________________________________________ #

# the hascontainer relationship methods have moved to relationshipDAO.py for now