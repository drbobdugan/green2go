import mysql.connector
from datetime import datetime
import logging
from relationship import Relationship
from DAO import dao
from datetime import timedelta
class RelationshipDAO(dao):

    # CREATE RELATIONSHIP
    def insertRelationship(self, r):
        try:
            """
            myresult = self.checkFormatting(r)
            if(myresult[0] == False):
                return myresult
            """
            logging.info("Entering insertRelationship")
            r.statusUpdateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
            result = r.relationshipToList()
            # change the old person's pending return status to verified return
            sql = "SELECT * from hascontainer WHERE qrcode = '" + result[1] + "' and status <> 'Verified Return' ORDER BY statusUpdateTime DESC"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            if(myresult[1] != [] and myresult[1] is not None):
                oldEmail = myresult[1][0]
                tempR = Relationship(oldEmail[0],oldEmail[1],oldEmail[2],oldEmail[3],oldEmail[4],"0",None)
                if(tempR.status=="Damaged Lost"):
                    return False, "Container has been marked as Damaged Lost"
                tempR.status="Verified Return"
                self.updateRelationship(tempR)

            sql = "INSERT INTO hascontainer (email,qrcode,status,statusUpdateTime,location_qrcode,active,description) VALUES (%s,%s,%s,%s,%s,%s,%s)"
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
            active = myresult[5]
            descrption = myresult[6]
            x = Relationship(email,qrcode,status,statusUpdateTime,location_qrcode,active,descrption)
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
                "location_qrcode": x[4],
                "active": x[5],
                "description": x[6]}
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
                "location_qrcode": x[4],
                "active": x[5],
                "description": x[6]}
                temp.append(relDict)
            logging.info("selectAllByStatus successful")
            return True, temp
        except Exception as e:
            logging.error("Error in selectAllByStatus")
            logging.error(str(e))
            return self.handleError(e)

    def selectAll(self): 
        try:
            logging.info("Entering selectAll") 
            sql = "SELECT * from hascontainer"
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
                "location_qrcode": x[4],
                "active": x[5],
                "description": x[6]}
                temp.append(relDict)
            logging.info("selectAll successful")
            return True, temp
        except Exception as e:
            logging.error("Error in selectAll")
            logging.error(str(e))
            return self.handleError(e)

    # UPDATE RELATIONSHIP
    def updateRelationship(self,r):
        try:
            """
            myresult = self.checkFormatting(r)
            if(myresult[0] == False):
                return myresult
            """
            logging.info("Entering updateRelationship")
            r.statusUpdateTime = (datetime.now() + timedelta(seconds=2)).strftime('%Y-%m-%d %H:%M:%S') 
            result = r.relationshipToList()
            sql = "SELECT * from hascontainer WHERE email = '" + result[0] + "' and qrcode = '" + result[1] + "' and status <> 'Verified Return'" + " ORDER BY statusUpdateTime DESC"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            myresult = myresult[1][0]
            myresult = list(myresult)
            myresult[3] = str(myresult[3])
            r1 = Relationship(myresult[0],myresult[1],myresult[2],myresult[3],myresult[4],myresult[5],myresult[6])
            if(r1.status=="Damaged Lost"):
                return False, "Container has been marked as Damaged Lost"
            sql = "UPDATE hascontainer SET status = '" + str(r.status) + "', location_qrcode = '" + str(r.location_qrcode) +"',  statusUpdateTime = '" + str(r.statusUpdateTime)+ "', active = '" + str(r.active)+ "', description = '" + str(r.description)+ "' WHERE email = '" + str(r1.email) + "' and " + "qrcode = '" + str(r1.qrcode) + "'" " and statusUpdateTime = '" + str(r1.statusUpdateTime) + "'"
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
            """
            print("here 1")
            myresult = self.checkFormatting(r)
            print(myresult[0])
            if(myresult[0] == False):
                return myresult
            print("here 2")
            """
            logging.info("Entering deleteRelationship")
            result = r.relationshipToList()
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
            print(str(e))
            logging.error(str(e))
            return self.handleError(e)
#____________________________________________________________________________________________________________

    # CHECK FORMATTING
    def checkFormatting(self,r):
        myresult = self.checkLength(r)
        if myresult[0] == False:
            return myresult
        return True, ""
    
    def checkLength(self,r):
        maxLength = {
        "email" : 45,
        "qrcode" : 45,
        "status" : 45,
        "location_qrcode" : 45,
        "active": 1,
        "description" : 128}

        var = "None"
        if(len(r.email)>maxLength["email"]):
            var = "email"
        if(len(r.qrcode)>maxLength["qrcode"]):
            var = "qrcode"
        if(len(r.status) > maxLength["status"]):
            var = "status"
        if(len(r.location_qrcode) > maxLength["location_qrcode"]):
            var = "location_qrcode"
        if(len(r.active) > maxLength["active"]):
            var = "active" 
        if(len(r.description) > maxLength["description"]):
            var = "description"

        if(var == "None"):
            return True, ""
        else:
            temp = var + " is too long, maximum length: " + str(maxLength[var])
            return False, temp