import mysql.connector
class HasContainerDao:

    def __init__(self):
        global mydb
        mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="sys") 

    #Accepts list val in format  val = () TOM's CODE
    def addRelationship(self, val):
        global mydb
        mycursor = mydb.cursor()
        sql = "INSERT INTO hascontainer (qrcode) VALUES (%s)" # TOM'S CODE
        mycursor.execute(sql, val)
        print(mycursor.rowcount, "record inserted.")
        mydb.commit()
    
    #Gets relationship (user:container) based on email+qrcode
    def getRelationship(self,qrcode):
        global mydb
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM hascontainer where email = '" + email + "' and qrcode = '" + qrcode + "'")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
   
    #Deletes container based on its qrcode
    def deleteRelationship(self,qrcode):
         global mydb
         mycursor = mydb.cursor()
         mycursor.execute("DELETE FROM hascontainer where email = '" + email + "' and qrcode = '" + qrcode + "'")
         mydb.commit()