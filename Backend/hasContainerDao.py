import mysql.connector
class HasContainerDao:

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

    #Accepts list val in format  val = (email, qrcode, status, statusUpdateTime)
    def addRelationship(self, val):  
        try:
             mycursor = self.mydb.cursor()
             sql = "INSERT INTO hascontainer (email,qrcode,status,statusUpdateTime) VALUES (%s,%s,%s,%s)"
             mycursor.execute(sql,val)
             print(mycursor.rowcount, "record inserted.")
             self.mydb.commit()
             return True
        except Exception as e:
            print(str(e))
            #return False
            self.reconnectSql()
            return self.addContainer(val)

    #Gets relationship based on email and qrcode 
    def getRelationship(self,val):
        try: 
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT * FROM hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "'")
            myresult = mycursor.fetchall()
            print(myresult)
            myresult = myresult[0]
            relDict={
                "email": myresult[0],
                "qrcode": myresult[1],
                "status": myresult[2],
                "statusUpdateTime": myresult[3]}
            return relDict
        except Exception as e:
            self.reconnectSql()
            return self.getRelationship(val)
            
    #Deletes relationship based on email and qrcode
    def deleteRelationship(self,val):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("DELETE FROM hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "'")
            self.mydb.commit()
            return True
        except:
            self.reconnectSql()
            return self.deleteRelationship(val)

    def updateRelationship(self,val):
        # for when status changes 
        def updateUser(self,userDict):
        mycursor = self.mydb.cursor()
        email = relDict["email"]
        qrcode = relDict["qrcode"]
        sqlSet = "UPDATE hasContainer SET "
        sqlWhere = "WHERE email = '" + email + "' and qrcode = '" + qrcode + "'"
        for key in userDict:
            if key == "email" or key=="qrcode" or key=="status" or key=="statusUpdateTime":
                pass
            elif userDict[key] is not None:
                sqlSet = sqlSet + str(key) + " = '" + str(relDict[key]) + "', "
        sqlSet = sqlSet[:-2]
        sqlSet += sqlWhere
        mycursor.execute(sqlSet)
        self.mydb.commit()
        return True