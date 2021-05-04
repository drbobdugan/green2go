import mysql.connector
from datetime import datetime
import logging
from appInfo import appInfo
from DAO import dao
class appInfoDAO(dao):

    def selectAppInfo(self):
        try:
            logging.info("Entering selectAppInfo")
            sql = "select * from appInfo"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            myresult = myresult[1][0]
            temp = appInfo(myresult[0],myresult[1],myresult[2])
            logging.info("selectAppInfo successful")
            return True, temp
        except Exception as e:
            logging.error("Error in selectAppInfo")
            logging.error(str(e))
            return self.handleError(e)

    def updateAppInfo(self,appInfoObject):
        try:
            logging.info("Entering updateAppInfo")
            myresult = self.deleteAppInfo()
            if(myresult[0] == False):
                return myresult
            myresult = self.insertAppInfo(appInfoObject)
            if(myresult[0] == False):
                return myresult
            return True, ""
        except Exception as e:
            logging.error("Error in updateAppInfo")
            logging.error(str(e))
            return self.handleError(e)

    def deleteAppInfo(self):
        try:
            logging.info("Entering deleteAppInfo")
            sql = "delete from appInfo"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            return True, ""
        except Exception as e:
            logging.error("Error in deleteAppInfo")
            logging.error(str(e))
            return self.handleError(e)

    def insertAppInfo(self,appInfoObject):
        try:
            logging.info("Entering insertAppInfo")
            sql = "insert into appInfo (major,minor,patch) values (%s,%s,%s)"
            myresult = self.handleSQL(sql,False,appInfoObject.appInfoToList())
            if(myresult[0] == False):
                return myresult
            logging.info("insertAppInfo successful")
            return True, ""
        except Exception as e:
            logging.error("Error in insertAppInfo")
            logging.error(str(e))
            return self.handleError(e)


