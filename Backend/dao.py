import mysql.connector
from datetime import datetime
import logging
class dao:
    def __init__(self):
        logging.basicConfig(filename='dao.log', level=logging.DEBUG)

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
    def disconnectedSql(self):
        try:
            self.mydb.shutdown()
        except:
            logging.error("Failed closing connection: Already disconnected")

    #  command , boolean for if you get something back, data to send to sql
    def handleSQL(self, sql, isReturn, package):
        try:
            self.reconnectSql()
            mycursor = self.mydb.cursor()
            mycursor = self.mydb.cursor(buffered=True)
            if package is None:
                mycursor.execute(sql)
            else:
                mycursor.execute(sql, package)
            if(isReturn == True):
                temp = mycursor.fetchall()
                mycursor.close()
                self.disconnectedSql()
                return True, temp
            else:
                self.mydb.commit()
                mycursor.close()
                self.disconnectedSql()
                return True, ""
        except Exception as e:
            logging.error("Error in handleSQL")
            logging.error(str(e))
            return self.handleError(e, mycursor)

          
    def handleError(self,error, cursor=None):
        if cursor is not None:
            cursor.close()
        error = str(error)
        if "Duplicate entry" in error:
            return False,"Duplicate Entry"
        if "Can't connect to MySQL server" in error:
            self.reconnectSql()
            return False, "Could not connect to database please try again"
        if "list index out of range" in error:
            return False, "Entry could not be found"