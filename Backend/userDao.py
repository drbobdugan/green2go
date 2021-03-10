from datetime import datetime
import logging
import mysql.connector
from dao import dao
class UserDao(dao):
    #Accepts list val in format  val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    #authTime and lastLogIn format (YYYY-MM-DD HH:MM:SS)
    def addUser(self, userDict):
        try:
            logging.info("Entering addUser")
            for key in userDict:
                if key == "middleName" or key =="classYear" or key=="auth_token":
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
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            val.append(time)
            val.append(time)
            sql = "INSERT INTO user (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode, authTime, lastLogIn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            myresult = self.handleSQL(sql,False, val)
            if(myresult[0] == False):
                return myresult
            logging.info("addUser successful")
            return True, ""
        except Exception as e:
            logging.error("Error in addUser")
            logging.error(str(e))
            return self.handleError(e)
    #Gets user based on their email
    def getUser(self,emailDict):
        try:
            logging.info("Entering getUser")
            email = emailDict["email"]
            sql = "SELECT * FROM user where email = '" + email + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            myresult = myresult[1][0]
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
            logging.info("getUser successful")
            return True, userDict
        except Exception as e:
            logging.error("Error in getUser")
            logging.error(str(e))
            return self.handleError(e)
    #Deletes user based on their email
    def updateUser(self,userDict):
        try:
            logging.info("Entering updateUser")
            email = userDict["email"]
            sqlSet = "UPDATE user SET "
            sqlWhere = "WHERE email = '"+email + "'"
            for key in userDict:
                if key == "email" or key == "auth_token":
                    pass
                elif userDict[key] is not None:
                    sqlSet = sqlSet + str(key) + " = '" + str(userDict[key]) + "', "
            sqlSet = sqlSet[:-2]
            sqlSet += sqlWhere
            myresult = self.handleSQL(sqlSet,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("updateUser successful")
            return True, ""
        except Exception as e:
            logging.error("Error in updateUser")
            logging.error(str(e))
            return self.handleError(e)
            #return self.deleteUser(email)
        
        
    def deleteUser(self,emailDict):
        email = emailDict["email"]
        if(self.getUser(emailDict)[0] == False):
            return False, "User does not exist"
        try:
            logging.info("Entering deleteUser")
            sql = "DELETE FROM user WHERE email like '" + email + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0]==False):
                return myresult
            logging.info("deleteUser successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteUser")
            logging.error(str(e))
            return self.handleError(e)
   