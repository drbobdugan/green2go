import mysql.connector
from datetime import datetime
import logging
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
    
    """
    # READ CONTAINER
    def selectContainer(self,c):
        try: 
            logging.info("Entering selectContainer")
            result = c.toContainerList()
            sql = "SELECT * FROM container WHERE qrcode = '" + result[0] + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            logging.info("selectContainer successful")
            return True, {"qrcode" : myresult[1][0][0]}
        except Exception as e:
            logging.error("Error in selectContainer")
            logging.error(str(e))
            return self.handleError(e)
        """
    """
    # UPDATE CONTAINER (idk if we need this method)
    def updateContainer(self,c):
        try:
            logging.info("Entering updateontainer")
            result = c.toContainerList()
            sql = "UPDATE container WHERE qrcode = '" + result[0] + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("updateContainer successful")
            return True, ""
        except Exception as e:
            logging.error("Error in updateContainer")
            logging.error(str(e))
            return self.handleError(e)
    """
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

    # CREATE RELATIONSHIP
    def insertRelationship(self, r):
        try:
            logging.info("Entering insertRelationship")
            result = r.toRelationshipList()
            result[3] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "SELECT * from hascontainer WHERE qrcode = '" + result[1] + "' and status <> 'Verified Return' ORDER BY statusUpdateTime DESC"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[1] != []):
                if(myresult[1] is not None):
                    oldEmail = myresult[1][0]
                    """
                    if (oldEmail[2]=="Pending Return"):
                         email=oldEmail[0],
                         qrcode=oldEmail[1],
                         status="Verified Return",
                         statusUpdateTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                         location_qrcode=oldEmail[4]
                         x = Relationship(email,qrcode,status,statusUpdateTime,None)
                        self.updateRelationship(x)
                    elif (oldEmail[2]=="Checked Out"):
                        return(False, "Container still checked out")
                    """
            sql = "INSERT INTO hascontainer (email,qrcode,status,statusUpdateTime,location_qrcode) VALUES (%s,%s,%s,%s,%s)"
            myresult = self.handleSQL(sql,False,result)
            if(myresult[0] == False):
                return myresult
            logging.info("insertRelationship successful")
            return True, ""
        except Exception as e:
            logging.error("Error in insertRelationship")
            logging.error(str(e))
            return self.handleError(e)

    """
    # READ RELATIONSHIP
    def selectRelationship(self,r):
        try: 
            logging.info("Entering selectRelationship")
            result = r.toRelationshipList()
            sqlSet = "SELECT * FROM hascontainer WHERE "
            # ??? bc our old for loop used a dictionary :(
            myresult = self.handleSQL(sqlSet,True,None)
            if(myresult[0] == False):
                return myresult
            myresult = myresult[1][0]
            email=myresult[0]
            qrcode=myresult[1]
            status=myresult[2]
            statusUpdateTime=str(myresult[3])
            location_qrcode=myresult[4]
            x = Relationship(email,qrcode,status,statusUpdateTime,location_qrcode)
            logging.info("selectRelationship successful")
            return True, x
        except Exception as e:
            logging.error("Error in selectRelationship")
            logging.error(str(e))
            return self.handleError(e)
        """

    def selectAllByEmail(self,r):
        try:
            logging.info("Entering selectAllByEmail")
            result = r.toRelationshipList()
            email = result[0] 
            #select all tuples from this user
            sql = "SELECT * from hascontainer WHERE email = '" + email + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            temp = []
            for x in myresult[1]:
                relDict={
                "qrcode": x[1],
                "status": x[2],
                "statusUpdateTime": str(x[3]),
                "location_qrcode": x[4]}
                temp.append(relDict)
            logging.info("selectAllByEmail successful")
            return True, temp
        except Exception as e:
            logging.error("Error in selectAllByEmail")
            logging.error(str(e))
            return self.handleError(e)  

    # previously called selectCheckedOut
    # should be thought of as selectAllByEmailAndStatus
    def selectAllByStatus(self,r):
        try:
            logging.info("Entering selectAllByStatus")
            result = r.toRelationshipList()
            email = result[0]
            status = result[2] 
            #select all tuples that are of this status from this user
            sql = "SELECT * from hascontainer WHERE email = '" + email + "' and status = '" + status + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            temp = []
            for x in myresult[1]:
                relDict={
                "email": x[0],
                "qrcode": x[1],
                "status": x[2],
                "statusUpdateTime": str(x[3]),
                "location_qrcode": x[4]}
                temp.append(relDict)
            logging.info("selectAllByStatus successful")
            return True, temp
        except Exception as e:
            logging.error("Error in selectAllByStatus")
            logging.error(str(e))
            return self.handleError(e)

    """
    # UPDATE RELATIONSHIP
    def updateRelationship(self,r):

    # DELETE RELATIONSHIP  
    def deleteRelationship(self,r):
    """