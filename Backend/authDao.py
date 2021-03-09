import mysql.connector
import json
import string
import random
from datetime import datetime, timedelta
class AuthDao:

    def __del__(self): 
        self.mydb.shutdown()
        
    def __init__(self):
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
            print("Already disconnected")
        self.mydb = mysql.connector.connect(
            host="198.199.77.174",
            user="root",
            password="Capstone2021!",
            database="sys",
            buffered=True)
    #accept dict of {email}
    def addAuth(self, dic):
        try:
            mycursor = self.mydb.cursor()
            val = []
            #user and primary key
            val.append(dic['email'])
            # auth and refresh codes
            val.append(dic["auth_token"])
            val.append(dic["refresh_token"])
            time = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
            val.append(time)
            sql = "INSERT INTO auth (user, auth_token, refresh_token, expires_at) VALUES (%s,%s,%s,%s)"
            mycursor.execute(sql, val)
            print(mycursor.rowcount, "record inserted.")
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            return True, {"user": dic["email"], "auth_token" : val[1], "refresh_token" : val[2], "expires_at" : val[3]}
        except Exception as e:
            print("Error in addAuth")
            print(str(e))
            return self.handleError(e, mycursor)
    #Gets user based on their email
    def getAuth(self,dic):
        try:
            mycursor = self.mydb.cursor()
            email = dic["email"]
            mycursor.execute("SELECT * FROM auth where user = '" + email + "'")
            myresult = mycursor.fetchall()
            if len(myresult) == 0:
                return False, "No matching user"
            myresult = myresult[0]
            res={
                "auth_token": myresult[1],
                "refresh_token": myresult[2],
                "expires_at": myresult[3].strftime('%Y-%m-%d %H:%M:%S'),
            }
            # close cursor 
            mycursor.close()
            return True, res
        except Exception as e:
            print("Error in getAuth")
            return self.handleError(e, mycursor)

    # only needs auth
    def updateAuth(self,dic):
        try:
            mycursor = self.mydb.cursor()
            email = dic["email"]
            token = dic["token"]
            timeV = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
            sql = "UPDATE auth set auth_token='" + str(token) +"', expires_at='" + str(timeV) + "' where user='" +str(email)+ "'"
            mycursor.execute(sql)
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            return True, {"auth_token" : str(token), "refresh_token" : dic["refresh_token"], "expires_at" : str(timeV)}
        except Exception as e:
            print("Error in updateAuth")
            return self.handleError(e, mycursor)
            #return self.deleteUser(email)
        
        
    def deleteAuth(self,dic):
        try:
            mycursor = self.mydb.cursor()
            email = dic["email"]
            if(self.getAuth(dic)[0] == False):
                return False, "No matching primary key"
            sql = "DELETE FROM auth WHERE user like '" + email + "'"
            mycursor.execute(sql)
            self.mydb.commit()
            # close cursor 
            mycursor.close()
            return True, ""
        except Exception as e:
            print("Error in deleteAuth")
            print(str(e))
            return self.handleError(e, mycursor)
            
    def handleError(self,error, cursor=None):
        if cursor is not None:
            cursor.close()
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