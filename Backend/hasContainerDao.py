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

    #Accepts list val in format  val = (email, qrcode, status, statusUpdateTime) Tom's dictionary? 
    def addRelationship(self, val):  
        try:
             mycursor = self.mydb.cursor()
             sql = "INSERT INTO hascontainer () VALUES (%s)"
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
            return {"relationship" : myresult[0][0]} #???
        except:
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