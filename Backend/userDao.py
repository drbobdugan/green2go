import mysql.connector
import json
from datetime import datetime
class UserDao:

    mydb = mysql.connector.connect(
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
    #Accepts list val in format  val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    #authTime and lastLogIn format (YYYY-MM-DD HH:MM:SS)
    def addUser(self, val):
        try:
            mycursor = self.mydb.cursor()
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # adding mock info
            val.append(111111)
            val.append(time)
            val.append(time)
            sql = "INSERT INTO user (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode, authTime, lastLogIn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sql, val)
            print(mycursor.rowcount, "record inserted.")
            self.mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
            #self.reconnectSql()
            #return self.addUser(val)
    #Gets user based on their email
    def getUser(self,email):
        try:
            mycursor = self.mydb.cursor()
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
        except:
            self.reconnectSql()
            return self.getUser(email)
    #Deletes user based on their email
    def updateUser(self,userDict):
        mycursor = self.mydb.cursor()
        email = userDict["email"]
        sqlSet = "UPDATE user SET "
        sqlWhere = "WHERE email = '"+email + "'"
        for key in userDict:
            if key == "email" or key=="authCode" or key=="authTime" or key=="classYear" or key=="lastLogIn":
                pass
            elif userDict[key] is not None:
                sqlSet = sqlSet + key + " = '" + userDict[key] + "' "
        sqlSet += sqlWhere
        print(sqlSet)
        
    def deleteUser(self,email):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("DELETE FROM user WHERE email = '" + email + "'")
            self.mydb.commit()
            return True
        except:
            self.reconnectSql()
            return self.deleteUser(email)
