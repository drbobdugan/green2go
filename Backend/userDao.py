import mysql.connector
import json
from datetime import datetime
import logging
class UserDao:

    def __init__(self):
        logging.basicConfig(filename='userDao.log', level=logging.DEBUG)
        self.mydb = mysql.connector.connect(
                host="198.199.77.174",
                user="root",
                password="Capstone2021!",
                database="sys",
                buffered=True) 
        
    def reconnectSql(self):
        try:
            self.mydb.shutdown()
        except:
            logging.error("Error closing connection: Already disconnected")
        self.mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="sys",
            buffered=True)
    #Accepts list val in format  val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    #authTime and lastLogIn format (YYYY-MM-DD HH:MM:SS)
    def addUser(self, userDict):
        try:
            logging.info("Entering addUser")
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
            tempRead = mycursor.rowcount
            self.mydb.commit()            
            # close cursor 
            mycursor.close()
            logging.info("addUser successful")
            return True, ""
        except Exception as e:
            logging.error("Error in addUser")
            logging.error(str(e))
            return self.handleError(e, mycursor)
    #Gets user based on their email
    def getUser(self,emailDict):
        mycursor = None
        try:
            logging.info("Entering getUser")
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
                "lastLogIn": str(myresult[10]),
                "authorized" : int(myresult[11])}
            # close cursor 
            mycursor.close()
            logging.info("getUser successful")
            return True, userDict
        except Exception as e:
            logging.error("Error in getUser")
            logging.error(str(e))
            return self.handleError(e, mycursor)
    #Deletes user based on their email
    def updateUser(self,userDict):
        try:
            logging.info("Entering updateUser")
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
            # close cursor 
            mycursor.close()
            logging.info("updateUser successful")
            return True, ""
        except Exception as e:
            logging.error("Error in updateUser")
            logging.error(str(e))
            return self.handleError(e, mycursor)
            #return self.deleteUser(email)
        
        
    def deleteUser(self,emailDict):
        email = emailDict["email"]
        if(self.userExists(emailDict)[0] == False):
            return False, "User does not exist"
        try:
            logging.info("Entering deleteUser")
            mycursor = self.mydb.cursor()
            sql = "DELETE FROM user WHERE email like '" + email + "'"
            mycursor.execute(sql)
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            logging.info("deleteUser successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteUser")
            logging.error(str(e))
            return self.handleError(e, mycursor)
    def userExists(self,emailDict):
        try:
            logging.info("Entering userExists")
            email = emailDict['email']
            mycursor = self.mydb.cursor()
            sql = "SELECT * FROM user where email = '" + email + "'"
            mycursor.execute(sql)
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
            # close cursor 
            mycursor.close()
            logging.info("userExists successful")
            return True, ""
        except Exception as e:
            logging.error("Error in userExists")
            logging.error(str(e))
            return self.handleError(e, mycursor)
            
    def handleError(self,error, cursor=None):
        if cursor is not None:
            cursor.close()
        error = str(error)
        logging.error(error)
        if "Duplicate entry" in error:
            return False,"Duplicate Entry"
        elif "Can't connect to MySQL server" in error:
            self.reconnectSql()
            return False, "Could not connect to database please try again"
        elif "list index out of range" in error:
            return False, "Entry could not be found"
        else:
            return False, error