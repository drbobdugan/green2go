import mysql.connector
from datetime import datetime
class ContainerDao:

    def __init__(self):
        
        self.mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="sys") 

    def reconnectSql(self):
        self.mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="sys")

    #Accepts dictionary that holds qr code
    def addContainer(self, contDict):  
        try:
             val = []
             val.append(contDict['qrcode'])
             mycursor = self.mydb.cursor()
             sql = "INSERT INTO container (qrcode) VALUE (%s)"
             mycursor.execute(sql,val)
             print(mycursor.rowcount, "record inserted.")
             self.mydb.commit()
             return True
        except Exception as e:
            print("Error in addContainer")
            return self.handleError(e)
            #return self.addContainer(val)
    
    #Gets container based on qrcode 
    def getContainer(self,qrcode):
        try: 
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT * FROM container WHERE qrcode = '" + qrcode + "'")
            myresult = mycursor.fetchall()
            return {"qrcode" : myresult[0][0]}
        except Exception as e:
            print("Error in getContainer")
            return self.handleError(e)
            
    #Deletes container based on qrcode
    #Can't connect to MySQL server
    def deleteContainer(self,qrcode):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("DELETE FROM container WHERE qrcode = '" + qrcode + "'")
            self.mydb.commit()
            return True
        except Exception as e:
            print("Error in deleteContainer")
            return self.handleError(e)
# ____________________________________________________________________________________________________ #

    #Accepts list val in format  val = (email, qrcode, status)
    def addRelationship(self, val):  
        try:
            mycursor = self.mydb.cursor()
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            val.append(str(time))
            qrcode = val[1]
            #if(self.containerExists(qrcode)!=True):
            #    return self.containerExists(qrcode)
            
            #search for old email code(lots of potenatial issues here)
            #myresult = mycursor.execute("SELECT * from hascontainer WHERE qrcode = '" + qrcode + "' ORDER BY statusUpdateTime")
            if(1==2):#myresult is not None):
                print("Dont be here")
                oldEmail = myresult[0][0]
                relDict={
                   "email": oldEmail,
                   "qrcode": val[1],
                   "status": "Verified Return",
                   "statusUpdateTime": time}
                self.updateRelationship(relDict)
            sql = "INSERT INTO hascontainer (email,qrcode,status,statusUpdateTime) VALUES (%s,%s,%s,%s)"
            mycursor.execute(sql,val)
            print("????")
            print(mycursor.rowcount, "record inserted.")
            self.mydb.commit()
            return True
        except Exception as e:
            print("Error in addRelationship")
            return self.handleError(e)

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
            #print(sqlSet)
            mycursor.execute(sqlSet)
            myresult = mycursor.fetchall()
            print(myresult)
            return True
        except Exception as e:
            print("Error in getRelationship")
            return self.handleError(e)
            
    #Deletes relationship based on email, qrcode, and status
    def deleteRelationship(self,val):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("DELETE FROM hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "' and status = '" + status + "'")
            self.mydb.commit()
            return True
        except Exception as e:
            print("Error in deleteRelationship")
            return self.handleError(e)

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
            print("MADE IT HERE")
            myresult = mycursor.execute("SELECT * from hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "' ORDER BY statusUpdateTime")
            print("MADE IT HERE")
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
            return True
        except Exception as e:
            print("Error in updateRelationship")
            return self.handleError(e)         
    def containerExists(self, qrcode):
        result = self.getContainer(qrcode)
        if len(result["qrcode"]) > 1:
            return True
        else:
            val = []
            val.append(qrcode)
            return self.addContainer(val)

    def handleError(self,error):
        error = str(error)
        if "Duplicate entry" in error:
            return False,"Duplicate Entry"
        if "Can't connect to MySQL server" in error:
            self.reconnectSql()
            return False, "Could not connect to database please try again"
        if "list index out of range" in error:
            return False, "Entry could not be found"