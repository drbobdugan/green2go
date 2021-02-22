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
            return self.addRelationship(val)

    #Gets relationship based on email and qrcode 
    def getRelationship(self,relDict): #backend passes a dict to database / some fields will be null
        try: 
            mycursor = self.mydb.cursor()
            email = relDict["email"]
            qrcode = relDict["qrcode"]
            status = relDict["status"]
            sqlSet = "SELECT * FROM hasContainer "
            sqlWhere = "WHERE " #email/email+qrcode/email+status/qrcode/qrcode+status/ or all three
            for key in relDict:
                if (key=="email") or : #???
                    pass
                elif relDict[key] is not None:
                    #
            sqlSet = sqlSet[:-2]
            sqlSet += sqlWhere
            mycursor.execute(sqlSet)
            self.mydb.commit()
            return True
        except Exception as e:
            self.reconnectSql()
            return False
            
    #Deletes relationship based on email, qrcode, and status
    def deleteRelationship(self,val):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("DELETE FROM hascontainer WHERE email = '" + email + "' and qrcode = '" + qrcode + "' and status = '" + status + "'")
            self.mydb.commit()
            return True
        except:
            self.reconnectSql()
            return self.deleteRelationship(val)

    # Update relationship (for when status changes)
    def updateRelationship(self,):
        # use same code from get relationship?