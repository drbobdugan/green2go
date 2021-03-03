import mysql.connector
from datetime import datetime
import logging
class ContainerDao:

    
    def __init__(self):
        logging.basicConfig(filename='containerDao.log', level=logging.DEBUG)
        self.mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="sys",
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
            database="sys",
            buffered=True)

    #Accepts dictionary that holds qr code
    def addContainer(self, contDict):  
        try:
            logging.info("Entering addContainer")
            val = []
            val.append(contDict['qrcode'])
            mycursor = self.mydb.cursor()
            sql = "INSERT INTO container (qrcode) VALUE (%s)"
            mycursor.execute(sql,val)
            temp = mycursor.rowcount
            logging.info("Container inserted.")
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            logging.info("addContainer successful")
            return True, ""
        except Exception as e:
            logging.error("Error in addContainer")
            logging.error(str(e))
            return self.handleError(e, mycursor)
            #return self.addContainer(val)
    
    #Gets container based on qrcode 
    def getContainer(self,qrcodeDict):
        try: 
            logging.info("Entering getContainer")
            qrcode=qrcodeDict['qrcode']
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT * FROM container WHERE qrcode = '" + qrcode + "'")
            myresult = mycursor.fetchall()
            # close cursor 
            mycursor.close()
            logging.info("getContainer successful")
            return True, {"qrcode" : myresult[0][0]}
        except Exception as e:
            logging.error("Error in getContainer")
            logging.error(str(e))
            return self.handleError(e, mycursor)
            
    #Deletes container based on qrcode
    #Can't connect to MySQL server
    def deleteContainer(self,qrcodeDict):
        try:
            logging.info("Entering deleteContainer")
            qrcode=qrcodeDict['qrcode']
            mycursor = self.mydb.cursor()
            mycursor.execute("DELETE FROM container WHERE qrcode = '" + qrcode + "'")
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            logging.info("deleteContainer successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteContainer")
            logging.error(str(e))
            return self.handleError(e, mycursor)

    
# ____________________________________________________________________________________________________ #

    #Accepts list val in format  val = (email, qrcode, status)
    #accepts dictionary with email qrcode and status
    def addRelationship(self, relDict):  
        try:
            val = []
            val.append(relDict['email'])
            val.append(relDict['qrcode'])
            val.append(relDict['status'])
            mycursor = self.mydb.cursor()
            mycursor = self.mydb.cursor(buffered=True)
            print("test1")
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            val.append(str(time))
            qrcode = val[1]
            #if(self.containerExists(qrcode)!=True):
            #    return self.containerExists(qrcode)
            
            #search for old email code(lots of potenatial issues here)
            myresult = mycursor.execute("SELECT * from hascontainer WHERE qrcode = '" + qrcode + "' ORDER BY statusUpdateTime ASC")
            if(myresult is not None):
                oldEmail = myresult[0][0]
                relDict={
                   "email": oldEmail,
                   "qrcode": val[1],
                   "status": "Verified Return",
                   "statusUpdateTime": time}
                self.updateRelationship(relDict)
            sql = "INSERT INTO hascontainer (email,qrcode,status,statusUpdateTime) VALUES (%s,%s,%s,%s)"
            mycursor.execute(sql,val)  #could break in the future
            temp = mycursor.rowcount
            logging.info("updateRelationship inserted.")
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            return True, ""
        except Exception as e:
            logging.error("Error in addRelationship")
            logging.error(str(e))
            return self.handleError(e, mycursor)

    #Gets relationship based on email and qrcode 
    def getRelationship(self,relDict): #backend passes a dict to database / some fields will be null
        try: 
            mycursor = self.mydb.cursor()
            sqlSet = "SELECT * FROM hascontainer WHERE "  #email/email+qrcode/email+status/qrcode/qrcode+status/ or all three
            for key in relDict:
                if relDict[key] is not None:
                    sqlSet = sqlSet + str(key) + "= '" + str(relDict[key]) + "' and "
                    #
            sqlSet = sqlSet[:-4]
            mycursor.execute(sqlSet)
            myresult = mycursor.fetchall()
            myresult = myresult[0]
            relDict={
                "email": myresult[0],
                "qrcode": myresult[1],
                "status": myresult[2],
                "statusUpdateTime": str(myresult[3])}
            # close cursor 
            mycursor.close()
            return True, relDict
        except Exception as e:
            logging.error("Error in getRelationship")
            logging.error(str(e))
            return self.handleError(e, mycursor)
            
    #Deletes relationship based on email, qrcode, and status
    def deleteRelationship(self,relDict):
        try:
            email = relDict["email"]
            qrcode = relDict["qrcode"]
            status = relDict["status"]
            mycursor = self.mydb.cursor()
            mycursor.execute("DELETE FROM hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "' and status = '" + status + "'")
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            return True, ""
        except Exception as e:
            logging.error("Error in deleteRelationship")
            logging.error(str(e))
            return self.handleError(e, mycursor)

    # Update relationship (for when status changes)
    #IMPORTANT NEED EMAIL AND QRCODE
    #order by time
    #add lost prevetion at some point
    def updateRelationship(self,relDict):
        try:
            #get all interaction sorted by time
            #extract newest entry time
            mycursor = self.mydb.cursor()
            email = relDict["email"]
            qrcode = relDict["qrcode"]
            #THIS DOES NOT WORK
            sql = "SELECT * from hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "'" 
            mycursor.execute(sql)#ORDER BY statusUpdateTime")
            myresult = mycursor.fetchall()
            statusUpdateTime = myresult[0][3]#Probably formatted wrong
            sqlSet = "UPDATE hascontainer SET "
            sqlWhere = "WHERE email = '"+email + "' and " + "qrcode = '"+qrcode + "'" " and statusUpdateTime = '" + statusUpdateTime + "'"
            for key in relDict:
                    if relDict[key] is not None:
                        sqlSet = sqlSet + str(key) + "= '" + str(relDict[key]) + "' , "
            sqlSet = sqlSet[:-2]
            sqlSet += sqlWhere
            mycursor.execute(sqlSet)
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            return True, ""
        except Exception as e:
            logging.error("Error in updateRelationship")
            logging.error(str(e))
            return self.handleError(e, mycursor)  

    def selectAllByEmail(self,emailDict):
        try:
            #select all containers from one user
            mycursor = self.mydb.cursor()
            email = emailDict["email"]
            sql = "SELECT * from hascontainer WHERE email = '" + email + "'"
            mycursor.execute(sql)#ORDER BY statusUpdateTime")
            myresult = mycursor.fetchall()
            mycursor.close()
            temp = []
            for x in myresult:
                relDict={
                "email": x[0],
                "qrcode": x[1],
                "status": x[2],
                "statusUpdateTime": str(x[3])}
                temp.append(relDict)
            return True, myresult
        except Exception as e:
            logging.error("Error in selectAllByEmail")
            logging.error(str(e))
            return self.handleError(e, mycursor)  

    def selectCheckedOut(self,relDict): 
        try:
            #select all containers from one user
            mycursor = self.mydb.cursor()
            email = relDict["email"]
            status = relDict["status"]
            sql = "SELECT * from hascontainer WHERE email = '" + email + "' and status = '" + status + "'"
            mycursor.execute(sql)#ORDER BY statusUpdateTime")
            myresult = mycursor.fetchall()
            mycursor.close()
            temp = []
            for x in myresult:
                relDict={
                "email": x[0],
                "qrcode": x[1],
                "status": x[2],
                "statusUpdateTime": str(x[3])}
                temp.append(relDict)
            return True, myresult
        except Exception as e:
            logging.error("Error in selectAllByEmail")
            logging.error(str(e))
            return self.handleError(e, mycursor)


    def containerExists(self, qrcodeDict):
        qrcode = qrcodeDict["qrcode"]
        result = self.getContainer(qrcodeDict)[1]
        if len(result["qrcode"]) > 1:
            return True, ""
        else:
            contDict={"qrcode": qrcode}
            return self.addContainer(contDict)

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