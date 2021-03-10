import mysql.connector
import json
import string
import random
import logging
from datetime import datetime, timedelta
from dao import dao
class AuthDao(dao):

    #accept dict of {email}
    def addAuth(self, dic):
        try:
            val = []
            #user and primary key
            val.append(dic['email'])
            # auth and refresh codes
            val.append(dic["auth_token"])
            val.append(dic["refresh_token"])
            time = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
            val.append(time)
            sql = "INSERT INTO auth (user, auth_token, refresh_token, expires_at) VALUES (%s,%s,%s,%s)"
            myresult = self.handleSQL(sql,False, val)
            if(myresult[0]==False):
                return myresult
            return True, {"user": dic["email"], "auth_token" : val[1], "refresh_token" : val[2], "expires_at" : val[3]}
        except Exception as e:
            logging.error("Error in addAuth")
            logging.error(str(e))
            return self.handleError(e)
    #Gets user based on their email
    def getAuth(self,dic):
        try:
            email = dic["email"]
            sql = "SELECT * FROM auth where user = '" + email + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0]==False):
                return myresult
            if len(myresult[1]) == 0:
                return False, "No matching user"
            logging.debug(myresult)
            myresult = myresult[1][0]
            res={
                "auth_token": myresult[1],
                "refresh_token": myresult[2],
                "expires_at": myresult[3].strftime('%Y-%m-%d %H:%M:%S'),
            }
            return True, res
        except Exception as e:
            logging.error("Error in getAuth")
            logging.error(str(e))
            return self.handleError(e)

    # only needs auth
    def updateAuth(self,dic):
        try:
            email = dic["email"]
            token = dic["token"]
            timeV = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
            sql = "UPDATE auth set auth_token='" + str(token) +"', expires_at='" + str(timeV) + "' where user='" +str(email)+ "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0]==False):
                return myresult
            return True, {"auth_token" : str(token), "refresh_token" : dic["refresh_token"], "expires_at" : str(timeV)}
        except Exception as e:
            logging.error("Error in updateAuth")
            logging.error(str(e))
            return self.handleError(e)
        
        
    def deleteAuth(self,dic):
        try:
            email = dic["email"]
            if(self.getAuth(dic)[0] == False):
                return False, "No matching primary key"
            sql = "DELETE FROM auth WHERE user like '" + email + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0]==False):
                return myresult
            return True, ""
        except Exception as e:
            logging.error("Error in deleteAuth")
            logging.error(str(e))
            return self.handleError(e)
            