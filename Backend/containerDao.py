import mysql.connector
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

    #Accepts list val in format  val = (qrcode)
    def addContainer(self, val):  
        try:
             mycursor = self.mydb.cursor()
             sql = "INSERT INTO container (qrcode) VALUE (%s)"
             mycursor.execute(sql,val)
             print(mycursor.rowcount, "record inserted.")
             self.mydb.commit()
             return True
        except Exception as e:
            print(str(e))
            #return False
            self.reconnectSql()
            return self.addContainer(val)
    #Gets container based on its qrcode 
    def getContainer(self,qrcode):
        try: 
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT * FROM container WHERE qrcode = '" + qrcode + "'")
            myresult = mycursor.fetchall()
            return {"qrcode" : myresult[0][0]}
        except:
            self.reconnectSql()
            return self.getContainer(qrcode)
            
    #Deletes container based on its qrcode
    def deleteContainer(self,qrcode):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("DELETE FROM container WHERE qrcode = '" + qrcode + "'")
            self.mydb.commit()
            return True
        except:
            self.reconnectSql()
            return self.deleteContainer(qrcode)