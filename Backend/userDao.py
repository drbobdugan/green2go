import mysql.connector
import json
class UserDao:

    def __init__(self):
        global mydb
        mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="sys") 
    #Accepts list val in format  val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    #authTime and lastLogIn format (YYYY-MM-DD HH:MM:SS)
    def addUser(self, val):
        try:
            global mydb
            mycursor = mydb.cursor()
            sql = "INSERT INTO user (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode, authTime, lastLogIn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sql, val)
            print(mycursor.rowcount, "record inserted.")
            mydb.commit()
            return True
        except:
            #Try to reconnect to the database
            reconnectSql()
            return False
    #Gets user based on their email
    def getUser(self,email):
        global mydb
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM user where email = '" + email + "'")
        myresult = mycursor.fetchall()
        myresult = myresult[0]
        userDict={
            "email": myresult[0],
            "password": myresult[1],
            "firstName": myresult[2],
            "lastName": myresult[3],
            "middleName": myresult[4],
            "phoneNum": myresult[5],
            "role": myresult[6],
            "classYear": myresult[7],
            "authCode": myresult[8],
            "authTime": myresult[9],
            "lastLogIn": myresult[10]}
        return userDict
    #Deletes user based on their email
    def deleteUser(self,email):
         global mydb
         mycursor = mydb.cursor()
         mycursor.execute("DELETE FROM user WHERE email = '" + email + "'")
         mydb.commit()
    def reconnectSql():
        global mydb
        mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="sys")
