import mysql.connector
from datetime import datetime
import logging
from dao import dao
class ContainerDao(dao):

    #Accepts dictionary that holds qr code
    def addContainer(self, contDict):  
        try:
            logging.info("Entering addContainer")
            val = []
            val.append(contDict['qrcode'])
            sql = "INSERT INTO container (qrcode) VALUE (%s)"
            myresult = self.handleSQL(sql,False,val)
            if(myresult[0] == False):
                return myresult
            logging.info("addContainer successful")
            return True, ""
        except Exception as e:
            logging.error("Error in addContainer")
            logging.error(str(e))
            return self.handleError(e)
    
    #Accepts dictionary that holds QR code
    def getContainer(self,qrcodeDict):
        try: 
            logging.info("Entering getContainer")
            qrcode=qrcodeDict['qrcode']
            sql = "SELECT * FROM container WHERE qrcode = '" + qrcode + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            logging.info("getContainer successful")
            return True, {"qrcode" : myresult[1][0][0]}
        except Exception as e:
            logging.error("Error in getContainer")
            logging.error(str(e))
            return self.handleError(e)
            
    #Accepts dictionary that holds qrcode
    def deleteContainer(self,qrcodeDict):
        try:
            logging.info("Entering deleteContainer")
            qrcode=qrcodeDict['qrcode']
            sql = "DELETE FROM container WHERE qrcode = '" + qrcode + "'"
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

    #accepts dictionary with email qrcode and status

    def addRelationship(self, relDict):  
        try:
            val = []
            val.append(relDict['email'])
            val.append(relDict['qrcode'])
            val.append(relDict['status'])
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            val.append(str(time))
            qrcode = val[1]
            sql = "SELECT * from hascontainer WHERE qrcode = '" + qrcode + "' and status <> 'Verified Return' ORDER BY statusUpdateTime DESC"
            myresult = self.handleSQL(sql,True,None)
            print(myresult)
            if(myresult[1] != []):
                if(myresult[1] is not None): # Check to make sure this is none
                    oldEmail = myresult[1][0]
                    if (oldEmail[2]=="Pending Return"):
                        relDict={
                         "email": oldEmail[0],
                         "qrcode": oldEmail[1],
                         "status": "Verified Return",
                          "statusUpdateTime": time}
                        print("here")
                        self.updateRelationship(relDict)
                    elif (oldEmail[2]=="Checked out"):
                        return("False", "Container already checked out")
            sql = "INSERT INTO hascontainer (email,qrcode,status,statusUpdateTime) VALUES (%s,%s,%s,%s)"
            myresult = self.handleSQL(sql,False,val)  #could break in the future
            if(myresult[0] == False):
                return myresult
            logging.info("updateRelationship inserted.")
            return True, ""
        except Exception as e:
            logging.error("Error in addRelationship")
            logging.error(str(e))
            return self.handleError(e)

    #Gets relationship based on email and qrcode 
    def getRelationship(self,relDict): #backend passes a dict to database / some fields will be null
        try: 
            sqlSet = "SELECT * FROM hascontainer WHERE "  #email/email+qrcode/email+status/qrcode/qrcode+status/ or all three
            for key in relDict:
                if relDict[key] is not None and key != "auth_token":
                    sqlSet = sqlSet + str(key) + "= '" + str(relDict[key]) + "' and "
            sqlSet = sqlSet[:-4]
            myresult = self.handleSQL(sqlSet,True,None)
            if(myresult[0] == False):
                return myresult
            myresult = myresult[1][0]
            relDict={
                "email": myresult[0],
                "qrcode": myresult[1],
                "status": myresult[2],
                "statusUpdateTime": str(myresult[3])}
            return True, relDict
        except Exception as e:
            logging.error("Error in getRelationship")
            logging.error(str(e))
            return self.handleError(e)
            
    #Deletes relationship based on email, qrcode, and status
    def deleteRelationship(self,relDict):
        try:
            email = relDict["email"]
            qrcode = relDict["qrcode"]
            status = relDict["status"]
            sql = "DELETE FROM hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "' and status = '" + status + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            return True, ""
        except Exception as e:
            logging.error("Error in deleteRelationship")
            logging.error(str(e))
            return self.handleError(e)

    # Update relationship (for when status changes)
    #IMPORTANT NEED EMAIL AND QRCODE
    #order by time
    #add lost prevetion at some point
    def updateRelationship(self,relDict):
        try:
            #get all interaction sorted by time
            #extract newest entry time
            email = relDict["email"]
            qrcode = relDict["qrcode"]
            status = relDict["status"]
            relDict["statusUpdateTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #THIS DOES NOT WORK
            sql = "SELECT * from hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "' and status <> 'Verified Return'" +"ORDER BY statusUpdateTime DESC"
            print(sql)
            myresult = self.handleSQL(sql,True,None)#ORDER BY statusUpdateTime")
            print (myresult)
            if(myresult[0] == False):
                return myresult
            if(type(myresult[1]) is list):
                statusUpdateTime = str(myresult[1][0][3])
            else:
                statusUpdateTime = str(myresult[1][3])
            sqlSet = "UPDATE hascontainer SET "
            sqlWhere = "WHERE email = '"+email + "' and " + "qrcode = '"+qrcode + "'" " and statusUpdateTime = '" + statusUpdateTime + "' and status <> 'Verified Return'"
            for key in relDict:
                    if relDict[key] is not None and key!="auth_token":
                        sqlSet = sqlSet + str(key) + "= '" + str(relDict[key]) + "' , "
            sqlSet = sqlSet[:-2]
            sqlSet += sqlWhere
            print(sqlSet)
            myresult = self.handleSQL(sqlSet,False,None)
            if(myresult[0] == False):
                return myresult
            return True, ""
        except Exception as e:
            logging.error("Error in updateRelationship")
            logging.error(str(e))
            return self.handleError(e)

    def selectAllByEmail(self,emailDict):
        try:
            #select all containers from one user
            email = emailDict["email"]
            sql = "SELECT * from hascontainer WHERE email = '" + email + "'"
            myresult = self.handleSQL(sql,True,None)#ORDER BY statusUpdateTime")
            if(myresult[0] == False):
                return myresult
            temp = []
            for x in myresult[1]:
                relDict={
                "email": x[0],
                "qrcode": x[1],
                "status": x[2],
                "statusUpdateTime": str(x[3])}
                temp.append(relDict)
            return True, temp
        except Exception as e:
            logging.error("Error in selectAllByEmail")
            logging.error(str(e))
            return self.handleError(e)  

    def selectCheckedOut(self,relDict): 
        try:
            #select all containers from one user
            email = relDict["email"]
            status = relDict["status"]
            sql = "SELECT * from hascontainer WHERE email = '" + email + "' and status = '" + status + "'"
            myresult = self.handleSQL(sql,True,None)#ORDER BY statusUpdateTime")
            if(myresult[0] == False):
                return myresult
            temp = []
            for x in myresult[1]:
                relDict={
                "email": x[0],
                "qrcode": x[1],
                "status": x[2],
                "statusUpdateTime": str(x[3])}
                temp.append(relDict)
            return True, temp
        except Exception as e:
            logging.error("Error in selectAllByEmail")
            logging.error(str(e))
            return self.handleError(e)