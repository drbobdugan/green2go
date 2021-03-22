from datetime import datetime
import logging
import mysql.connector
from DAO import dao
from user import User
class UserDao(dao):
    #Accepts list val in format  val = (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode,authTime,lastLogIn)
    #authTime and lastLogIn format (YYYY-MM-DD HH:MM:SS)
    def addUser(self, user):
        try:
            logging.info("Entering addUser")
            #FOR BACKEND -> datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "INSERT INTO user (email, password, firstName, lastName, middleName, phoneNum, role, classYear, authCode, authTime, lastLogIn,authorized) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            myresult = self.handleSQL(sql,False, user.userToList())
            if(myresult[0] == False):
                return myresult
            logging.info("addUser successful")
            return True, ""
        except Exception as e:
            logging.error("Error in addUser")
            logging.error(str(e))
            return self.handleError(e)
    #Gets user based on their email
    def getUser(self,email):
        try:
            logging.info("Entering getUser")
            sql = "SELECT * FROM user where email = '" + email + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            myresult = myresult[1][0]
            user = User(myresult[0], 
                        myresult[1], 
                        myresult[2], 
                        myresult[3], 
                        myresult[4], 
                        myresult[5],
                        myresult[6], 
                        str(myresult[7]),
                        myresult[8], 
                        str(myresult[9]), 
                        str(myresult[10]),
                        str(myresult[11]))
            logging.info("getUser successful")
            return True, user
        except Exception as e:
            logging.error("Error in getUser")
            logging.error(str(e))
            return self.handleError(e)
    #FOR BACKEND -> BEFORE CALLING UPDATE PLEASE DO A GETUSER CALL SO THAT ALL OF THE VALUES ARE FILLED OUT
    def updateUser(self,user):
        try:
            logging.info("Entering updateUser")
            myresult = self.deleteUser(user)
            if(myresult[0] == False):
                return myresult
            myresult = self.addUser(user)
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
            email = user.email
            myresult = self.getUser(email)
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
   