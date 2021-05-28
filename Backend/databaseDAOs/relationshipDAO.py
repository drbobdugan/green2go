import mysql.connector
import logging
from userDAO import UserDAO
from relationship import Relationship
from DAO import dao
from datetime import datetime
from datetime import timedelta

class RelationshipDAO(dao):

    def getRecentUser(self, qrcode):
        try:
            logging.info("Entering getRecentUser")
            sql = "SELECT * from hascontainer WHERE qrcode = '" + qrcode + "' and status <> 'Verified Return' ORDER BY statusUpdateTime DESC"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            if(myresult[1] != [] and myresult[1] is not None):
                logging.info("getRecentUser successful")
                return True, myresult[1][0][0]
            return False, "Could not find relationship with that QR code"
        except Exception as e:
            logging.error("Error in getRecentUser")
            logging.error(str(e))
            return self.handleError(e)
            
    def changeOldRelationship(self,result):
        try:
            logging.info("Entering changeOldRelationship")
            sql = "SELECT * from hascontainer WHERE qrcode = '" + result[1] + "' and status <> 'Verified Return' ORDER BY statusUpdateTime DESC"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                   return myresult
            if(myresult[1] != [] and myresult[1] is not None):
                oldEmail = myresult[1][0]
                tempR = Relationship(oldEmail[0],oldEmail[1],oldEmail[2],oldEmail[3],oldEmail[4], None)
                if(tempR.status=="Damaged Lost"):
                    tempR.description = ""
                    #return False, "Container has been marked as Damaged Lost"
                #if(result[2] != "Damaged Lost"):
                tempR.status="Verified Return"
                self.updateRelationship(tempR)
        except Exception as e:
            logging.error("Error in changeOldRelationship")
            logging.error(str(e))
            return self.handleError(e)
    
    # CREATE RELATIONSHIP
    def insertRelationship(self, r):
        try:
            logging.error("Entering changeOldRelationship")
            myresult = self.checkStatus(r)
            if(myresult[0] == False):
                return myresult
            logging.info("Entering insertRelationship")
            result = r.relationshipToList()
            # change the old person's pending return status to verified return
            if(r.status != "Damaged Lost"):
                self.changeOldRelationship(result)
            sql = "INSERT INTO hascontainer (email,qrcode,status,statusUpdateTime,location_qrcode,description) VALUES (%s,%s,%s,%s,%s,%s)"
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
            descrption = myresult[5]
            x = Relationship(email,qrcode,status,statusUpdateTime,location_qrcode,descrption)
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
                email=x[0]
                qrcode=x[1]
                status=x[2]
                statusUpdateTime=str(x[3])
                location_qrcode=x[4]
                descrption = x[5]
                r = Relationship(email,qrcode,status,statusUpdateTime,location_qrcode,descrption)
                temp.append(r)
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
                email=x[0]
                qrcode=x[1]
                status=x[2]
                statusUpdateTime=str(x[3])
                location_qrcode=x[4]
                descrption = x[5]
                r = Relationship(email,qrcode,status,statusUpdateTime,location_qrcode,descrption)
                temp.append(r)
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
                email=x[0]
                qrcode=x[1]
                status=x[2]
                statusUpdateTime=str(x[3])
                location_qrcode=x[4]
                descrption = x[5]
                r = Relationship(email,qrcode,status,statusUpdateTime,location_qrcode,descrption)
                temp.append(r)
            logging.info("selectAll successful")
            return True, temp
        except Exception as e:
            logging.error("Error in selectAll")
            logging.error(str(e))
            return self.handleError(e)

    def selectPendingReturns(self): 
        try: 
            logging.info("Entering selectPendingReturns")
            sql = "SELECT * from hascontainer WHERE status = 'Pending Return' "
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            #myresult = myresult[1]
            #print(myresult)
            temp = []
            for x in myresult[1]:
                email=x[0]
                qrcode=x[1]
                status=x[2]
                statusUpdateTime=str(x[3])
                location_qrcode=x[4]
                descrption = x[5]
                r = Relationship(email,qrcode,status,statusUpdateTime,location_qrcode,descrption)
                temp.append(r)
            #print(temp)
            logging.info("selectPendingReturns successful")
            return True, temp
        except Exception as e:
            logging.error("Error in selectPendingReturns")
            logging.error(str(e))
            return self.handleError(e)

    #DELETE THIS
    def selectActiveQRcode(self,qrcode):
        try: 
            logging.info("Entering selectActiveQRcode")
            sql = "SELECT * from hascontainer WHERE qrcode = '" + qrcode + "' and status != 'Verified Return'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            #myresult = myresult[1]
            temp = []
            for x in myresult[1]:
                email=x[0]
                qrcode=x[1]
                status=x[2]
                statusUpdateTime=str(x[3])
                location_qrcode=x[4]
                descrption = x[5]
                r = Relationship(email,qrcode,status,statusUpdateTime,location_qrcode,descrption)
                temp.append(r)
            logging.info("selectActiveQRcode successful")
            return True, temp
        except Exception as e:
            logging.error("Error in selectActiveQRcode")
            logging.error(str(e))
            return self.handleError(e)


    # UPDATE RELATIONSHIP
    def updateRelationship(self,r): 
        try:
            myresult = self.checkStatus(r)
            if(myresult[0] == False):
                return myresult
            logging.info("Entering updateRelationship")
            #r.statusUpdateTime = (r.statusUpdateTime + timedelta(seconds = 2)).strftime('%Y-%m-%d %H:%M:%S')
            #if status is Pending Return, call updatePoints()

                
            result = r.relationshipToList()
            #sql = "SELECT * from hascontainer WHERE email = '" + result[0] + "' and qrcode = '" + result[1] + "' and status <> 'Verified Return'" + " ORDER BY statusUpdateTime DESC"
            sql = "SELECT * from hascontainer WHERE qrcode = '" + result[1] + "' and status != 'Verified Return'"
            myresult = self.handleSQL(sql,True,None)
            #print(myresult,"here")
            if(myresult[0] == False):
                return myresult
            myresult = myresult[1][0]
            myresult = list(myresult)
            myresult[3] = str(myresult[3])
            
            r1 = Relationship(myresult[0],myresult[1],myresult[2],myresult[3],myresult[4],myresult[5])
            
                  #if(r1.status=="Damaged Lost"):
                #return False, "Container has been marked as Damaged Lost"
                 #if(r.status == "Damaged Lost" and r.description == None):
                #return False, "Damaged Lost Container lacks description"
            sql = "UPDATE hascontainer SET status = '" + str(r.status) + "', location_qrcode = '" + str(r.location_qrcode) +"',  statusUpdateTime = '" + str(r.statusUpdateTime)+ "', description = '" + str(r.description)+ "' WHERE email = '" + str(r1.email) + "' and " + "qrcode = '" + str(r1.qrcode) + "'" " and statusUpdateTime = '" + str(r1.statusUpdateTime) + "'"
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
    
    def checkStatus(self,r):
        if(r.status == "Checked Out" or r.status == "Pending Return" or r.status == "Verified Return" or r.status == "Damaged Lost"):
            return True, ""
        return False, "Invalid Status"


    #Returns true if container is checked out (and email matches passed email). 
    def isCheckedOut(self,email,qrcode):
        logging.info("Entering isCheckedOut")
        try:
            sql = "SELECT * from hascontainer WHERE qrcode = '" + qrcode + "' and status = 'Checked Out'"
            result = self.handleSQL(sql,True,None)
            logging.info("%s Result successful",result[1])
            if(result[1] == []):
                logging.info("Result is empty")
                return False, "container doesn't exist"
            else:
                logging.info("Result is full")
                return True, "container exists"
        except Exception as e:
            logging.info("Exception")
            return False, "error"

    def checkLength(self,r):
        maxLength = {
        "email" : 45,
        "qrcode" : 45,
        "status" : 45,
        "location_qrcode" : 45,
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
        if(len(r.description) > maxLength["description"]):
            var = "description"

        if(var == "None"):
            return True, ""
        else:
            temp = var + " is too long, maximum length: " + str(maxLength[var])
            return False, temp
