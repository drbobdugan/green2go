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
    def addUser(self, userDict):
        try:
            for key in userDict:
                if key == "middleName" or key =="classYear":
                    pass
                elif userDict[key] is None:
                    string = "Missing " + str(userDict[key])
                    return False, string
            val = []
            val.append(userDict['email'])
            val.append(userDict['password'])
            val.append(userDict['firstName'])
            val.append(userDict['lastName'])
            val.append(userDict['middleName'])
            val.append(userDict['phoneNum'])
            val.append(userDict['role'])
            val.append(userDict['classYear'])
            val.append(userDict['authCode'])
            mycursor = self.mydb.cursor()
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            val.append(time)
            val.append(time)
            sql = "INSERT INTO user (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode, authTime, lastLogIn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sql, val)
            print(mycursor.rowcount, "record inserted.")
            self.mydb.commit()
            return True, ""
        except Exception as e:
            print("Error in addUser")
            print(str(e))
            return self.handleError(e)
    #Gets user based on their email
    def getUser(self,emailDict):
        try:
            email = emailDict["email"]
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
                "classYear": str(myresult[7]),
                "authCode": myresult[8],
                "authTime": str(myresult[9]),
                "lastLogIn": str(myresult[10])}
            return True, userDict
        except Exception as e:
            print("Error in getUser")
            return self.handleError(e)
    #Deletes user based on their email
    def updateUser(self,userDict):
        try:
            mycursor = self.mydb.cursor()
            email = userDict["email"]
            sqlSet = "UPDATE user SET "
            sqlWhere = "WHERE email = '"+email + "'"
            for key in userDict:
                if key == "email":
                    pass
                elif userDict[key] is not None:
                    sqlSet = sqlSet + str(key) + " = '" + str(userDict[key]) + "', "
            sqlSet = sqlSet[:-2]
            sqlSet += sqlWhere
            mycursor.execute(sqlSet)
            self.mydb.commit()
            return True, ""
        except Exception as e:
            print("Error in updateUser")
            return self.handleError(e)
            #return self.deleteUser(email)
        
        
    def deleteUser(self,emailDict):
        email = emailDict["email"]
        if(self.userExists(emailDict)[0] == False):
            return False, "User does not exist"
        try:
            mycursor = self.mydb.cursor()
            sql = "DELETE FROM user WHERE email like '" + email + "'"
            print("SQL deleteUser ",sql)
            mycursor.execute(sql)
            self.mydb.commit()
            return True, ""
        except Exception as e:
            print("Error in deleteUser")
            print(str(e))
            return self.handleError(e)
    def userExists(self,emailDict):
        try:
            email = emailDict['email']
            print(email)
            mycursor = self.mydb.cursor()
            sql = "SELECT * FROM user where email = '" + email + "'"
            print("SQL STATEMENT: ",sql)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            myresult = myresult[0]
            print(myresult)
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
            return True, ""
        except Exception as e:
            print("Error in userExists")
            print(str(e))
            return self.handleError(e)
            
    def handleError(self,error):
        error = str(error)
        print(error)
        if "Duplicate entry" in error:
            return False,"Duplicate Entry"
        elif "Can't connect to MySQL server" in error:
            self.reconnectSql()
            return False, "Could not connect to database please try again"
        elif "list index out of range" in error:
            return False, "Entry could not be found"
        else:
            return False, error