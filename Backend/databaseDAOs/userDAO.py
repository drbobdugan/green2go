from datetime import datetime
import logging
import mysql.connector
from DAO import dao
from user import User
class UserDAO(dao):
    #datetime format is (YYYY-MM-DD HH:MM:SS)

    def checkFormatting(self,user):
        if(user.email is None or user.password is None or user.firstName is None or user.lastName is None or user.phoneNum is None or user.role is None or user.authCode is None or user.authTime is None or user.lastLogIn is None or user.authorized is None or user.beams_token is None or user.points is None):
            return False, "Unauthorized NoneType variable"
        myresult = self.checkLength(user)
        if myresult[0] == False:
            return myresult
        return True, ""
    def checkLength(self,user):
        maxLength = {
        "email" : 45,
        "password" : 100,
        "firstName" : 45,
        "lastName" : 45,
        "middleName" : 45,
        "phoneNum" : 15,
        "role" : 45,
        "authCode" : 45,
        "authorized" : 1,
        "beams_token" : 400,
        "points" : 11}
        var = "None"
        if(len(user.email)>maxLength["email"]):
            var = "email"
        if(len(user.password)>maxLength["password"]):
            var = "password"
        if(len(user.firstName) > maxLength["firstName"]):
            var = "firstName"
        if(len(user.lastName) > maxLength["lastName"]):
            var = "lastName"
        if(len(user.middleName) > maxLength["middleName"]):
            var = "middleName"
        if(len(user.phoneNum) > maxLength["phoneNum"]):
            var = "phoneNum"
        if(len(user.role) > maxLength["role"]):
            var = "role"
        if(len(user.authCode) > maxLength["authCode"]):
            var = "authCode"
        if(len(user.authorized) > maxLength["authorized"]):
            var = "authorized"
        if(len(user.beams_token) > maxLength["beams_token"]):
            var = "beams_token"
        if(len(str(user.points)) > maxLength["points"]):
            var = "points"
        if(var == "None"):
            return True, ""
        else:
            temp = var + " is too long, maximum length: " + str(maxLength[var])
            return False, temp  

    def insertUser(self, user):
        try:
            logging.info("Entering insertUser")
            myresult = self.checkFormatting(user)
            if(myresult[0] == False):
                return myresult
            user.lastLogIn = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "INSERT INTO user (email, password, firstName, lastName, middleName, phoneNum, role, authCode, authTime, lastLogIn,authorized,beams_token,points,reward_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            myresult = self.handleSQL(sql,False, user.userToList())
            if(myresult[0] == False):
                return myresult
            logging.info("insertUser successful")
            return True, ""
        except Exception as e:
            logging.error("Error in insertUser")
            logging.error(str(e))
            return self.handleError(e)
    
    #Gets user based on their email
    def selectUser(self,email):
        try:
            logging.info("Entering selectUser")
            sql = "SELECT * FROM user where email = '" + email + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            myresult = myresult[1][0]
            user = User(myresult[0], myresult[1], myresult[2], myresult[3], myresult[4], myresult[5],myresult[6],myresult[7], str(myresult[8]), str(myresult[9]),str(myresult[10]),myresult[11],myresult[12],str(myresult[13]))
            logging.info("selectUser successful")
            return True, user
        except Exception as e:
            logging.error("Error in selectUser")
            logging.error(str(e))
            return self.handleError(e)
    
    def selectAll(self): #returns --> "true, list of user objects"
        try:
            logging.info("Entering selectAll")
            sql = "SELECT * FROM user"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0]==False):
                return myresult
            result = []
            for row in myresult[1]:
                user = User(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7], str(row[8]), str(row[9]),str(row[10]),row[11],row[12],str(row[13]))
                result.append(user)
            logging.info("Successful selectAll")
            return True, result
        except Exception as e:
            logging.error("Error in selectAll")
            logging.error(str(e))
            return self.handleError(e)
    
    #FOR BACKEND -> BEFORE CALLING UPDATE PLEASE DO A GETUSER CALL SO THAT ALL OF THE VALUES ARE FILLED OUT
    def updateUser(self,user):
        try:
            myresult = self.checkFormatting(user)
            if(myresult[0] == False):
                return myresult
            logging.info("Entering updateUser")
            sql = "UPDATE user set password = '" + user.password + "', firstName = '" + user.firstName + "', lastName ='" + user.lastName + "', middleName = '" + user.middleName + "', phoneNum = '" + user.phoneNum + "', role = '" + user.role + "', authCode = '" + user.authCode + "', authTime = '" + user.authTime + "', lastLogIn = '" + user.lastLogIn + "', authorized = '" + user.authorized + "', beams_token = '" + user.beams_token + "', points = '" + str(user.points) + "', reward_date = '" + str(user.reward_date) + "' where email = '" + user.email + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            return True, ""
        except Exception as e:
            logging.error("Error in updateUser")
            logging.error(str(e))
            return self.handleError(e)
            #return self.deleteUser(email)
    
    def deleteUser(self,user): #DELETE THEIR ENTRY IN THE AUTH TABLE
        try:
            myresult = self.checkFormatting(user)
            if(myresult[0] == False):
                return myresult
            email = user.email
            myresult = self.selectUser(email)
            if(myresult[0]==False):
                return myresult
            logging.info("Entering deleteUser")
            sql = "DELETE FROM user WHERE email = '" + email + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0]==False):
                return myresult
            logging.info("deleteUser successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteUser")
            logging.error(str(e))
            return self.handleError(e)
   