import mysql.connector
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
        global mydb
        mycursor = mydb.cursor()
        sql = "INSERT INTO user (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode, authTime, lastLogIn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql, val)
        print(mycursor.rowcount, "record inserted.")
        mydb.commit()
    #Gets user based on their email
    def getUser(self,email):
        global mydb
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM user where email = '" + email + "'")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
    #Deletes user based on their email
    def deleteUser(self,email):
         global mydb
         mycursor = mydb.cursor()
         mycursor.execute("DELETE FROM user WHERE email = '" + email + "'")
         mydb.commit()