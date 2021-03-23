import mysql.connector
from datetime import datetime
import logging
from relationship import Relationship
from DAO import dao
class RelationshipDAO(dao):

    # CREATE RELATIONSHIP
    def insertRelationship(self, r):
        try:

            logging.info("Entering insertRelationship")
            r.statusUpdateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = r.toRelationshipList()
            # change the old person's pending return status to verified return
            sql = "SELECT * from hascontainer WHERE qrcode = '" + result[1] + "' and status <> 'Verified Return' ORDER BY statusUpdateTime DESC"
            #print("SQL:", sql)
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            if(myresult[1] != [] and myresult[1] is not None):
                oldEmail = myresult[1][0]
                tempR = Relationship(oldEmail[0],oldEmail[1],oldEmail[2],oldEmail[3],oldEmail[4])
                tempR.status="Verified Return"
                self.updateRelationship(tempR) # update isn't finished yet tho

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

    # READ RELATIONSHIP
    def selectRelationship(self,email,qrcode): 
        try: 
            logging.info("Entering selectRelationship")
            sql = "SELECT * from hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "' ORDER BY statusUpdateTime DESC"
            myresult = self.handleSQL(sql,True,None)
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

    def selectAllByEmail(self,email):
        try:
            logging.info("Entering selectAllByEmail")
            #select all tuples that are from this one user
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
    def selectAllByStatus(self,email,status): 
        try:
            logging.info("Entering selectAllByStatus") 
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

    # UPDATE RELATIONSHIP
    def updateRelationship(self,r):
        try:
            logging.info("Entering updateRelationship")
            r.statusUpdateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = r.toRelationshipList()
            sql = "SELECT * from hascontainer WHERE email = '" + result[0] + "' and qrcode = '" + result[1] + "' and status <> 'Verified Return'" + " ORDER BY statusUpdateTime DESC"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            myresult = myresult[1][0]
            sql = "UPDATE hascontainer SET status = 'Verifed Return' WHERE email = '" + result[0] + "' and " + "qrcode = '" + result[1] + "'" " and statusUpdateTime = '" + str(myresult[3]) + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            return True, ""
        except Exception as e:
            logging.error("Error in updateRelationship")
            logging.error(str(e))
            return self.handleError(e)

    # DELETE RELATIONSHIP  
    def deleteRelationship(self,r):
        try:
            logging.info("Entering deleteRelationship")
            result = r.toRelationshipList()
            email = result[0]
            qrcode = result[1]
            status = result[2] 
            sql = "DELETE FROM hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "' and status = '" + status + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("deleteRelationship successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteRelationship")
            logging.error(str(e))
            return self.handleError(e)