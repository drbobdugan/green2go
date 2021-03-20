import mysql.connector
import json
import string
import random
import logging
from datetime import datetime, timedelta
from DAO import dao
from auth import Auth
class AuthDao(dao):
    #the user field in Auth Table is the user's email
    def insertAuth(self,auth):
        try:
            logging.info("Entering insertAuth")
            result = auth.toAuthList()
            sql = "INSERT INTO auth (user,auth_token,refresh_token,expires_at) VALUES (%s,%s,%s,%s)"
            myresult = self.handleSQL(sql,False,result)
            if(myresult[0] == False):
                return myresult
            logging.info("insertAuth successful")
            return True, ""
        except Exception as e:
            logging.error("Error in insertAuth")
            logging.error(str(e))
            return self.handleError(e)
    
    def selectByEmail(self,email): #returns --> "true, specific auth object by email"
        try:
            logging.info("Entering selectByEmail")
            sql = "SELECT * FROM auth WHERE user = '" + email + "'"
            myresult = self.handleSQL(sql,True,None)
            print("myresult: ",myresult)
            if(myresult[0]==False):
                return myresult 
            myresult2 = myresult[1][0] #myresult looks like (true,[(user,auth_token,refresh_token,expires_at)])
            print("myresult2: ",myresult2)
            auth = Auth(myresult2[0],myresult2[1],myresult2[2],myresult[3])
            print(auth.getUser)
            print(auth.auth_token)
            print(auth.refresh_token)
            print(auth.expires_at)
            return True, auth
        except Exception as e:
            logging.error("Error in selectByEmail")
            logging.error(str(e))
            return self.handleError(e)

    def updateAuth(self,auth):
        try:
            email = auth.user
            token = auth.auth_token
            timeV = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
            sql = "UPDATE auth set auth_token='" + str(token) +"', expires_at='" + str(timeV) + "' where user='" +str(email)+ "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0]==False):
                return myresult
            auth = Auth(myresult[0],myresult[1],myresult[2],myresult[3])
            return True, auth
        except Exception as e:
            logging.error("Error in updateAuth")
            logging.error(str(e))
            return self.handleError(e)

    def deleteAuth(self,auth):
        try:
            logging.info("Entering deleteAuth")
            sql = "DELETE FROM auth WHERE user = '" + auth.getUser() + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("deleteAuth successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteAuth")
            logging.error(str(e))
            return self.handleError(e)