import mysql.connector
class ContainerDao:

    def __init__(self):
        global mydb
        mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="sys") 
    #Accepts list val in format  val = (qrcode)
    def addContainer(self, val):
        global mydb
        mycursor = mydb.cursor()
        sql = "INSERT INTO container (qrcode) VALUES (%s)"
        mycursor.execute(sql, val)
        print(mycursor.rowcount, "record inserted.")
        mydb.commit()
    #Gets container based on its qrcode 
    def getContainer(self,qrcode):
        global mydb
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM container WHERE qrcode = '" + qrcode + "'")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
    #Deletes container based on its qrcode
    def deleteContainer(self,qrcode):
         global mydb
         mycursor = mydb.cursor()
         mycursor.execute("DELETE FROM container WHERE qrcode = '" + qrcode + "'")
         mydb.commit()