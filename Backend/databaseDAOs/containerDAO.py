import mysql.connector
from datetime import datetime
import logging
from container import Container
from DAO import dao
class ContainerDAO(dao):


    def totalContainersDamagedLost(self):
        try:
            logging.info("Entering totalDamagedLostContainers")
            sql = "select distinct email, qrcode, statusUpdateTime, hascontainer.location_qrcode from hascontainer where hascontainer.status = 'Damaged Lost'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            temp = []
            for result in myresult[1]:
                temp.append({"email":result[0],"qrcode":result[1],"statusUpdateTime":str(result[2])})
            print(temp)
            return True, temp
        except Exception as e:
            logging.error("Error in totalDamagedLostContainers")
            logging.error(str(e))
            return self.handleError(e)

    def totalContainersCheckedOut(self):
        try:
            logging.info("Entering totalCheckedOutContainers")
            sql = "select distinct email, qrcode, statusUpdateTime, hascontainer.location_qrcode from hascontainer where hascontainer.status = 'Checked Out'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            temp = []
            for result in myresult[1]:
                temp.append({"email":result[0],"qrcode":result[1],"statusUpdateTime":str(result[2])})
            return True, temp
        except Exception as e:
            logging.error("Error in totalCheckedOutContainers")
            logging.error(str(e))
            return self.handleError(e)

            
    def selectRecentStatus(self):
        try:
            logging.info("Entering selectRecentStatus")
            #sql = "SELECT container.qrcode, hascontainer.status, container.name FROM container LEFT JOIN hascontainer ON container.qrcode = hascontainer.qrcode"
            sql = "SELECT container.qrcode, hascontainer.status FROM container LEFT JOIN hascontainer ON container.qrcode = hascontainer.qrcode"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            temp = []
            for result in myresult[1]:
                qrcode = result[0]
                try:
                    status = result[1]
                except:
                    status = None
                #try:
                #    name = result[2]
                #except:
                #    name = None
                if status != 'Verified Return':
                    temp.append({"qrcode":qrcode,"status":status})
                    #temp.append({"qrcode":qrcode,"name":name,"status":status})
            return True, temp
        except Exception as e:
            logging.error("Error in selectRecentStatus")
            logging.error(str(e))
            return self.handleError(e)
        
    def totalContainersInBins(self):
        try:
            logging.info("Entering totalContainersInBins")
            sql = "select email, qrcode, statusUpdateTime, hascontainer.location_qrcode from hascontainer, location where hascontainer.status = 'Pending Return' and location.lastPickup < hascontainer.statusUpdateTime and location.location_qrcode = hascontainer.location_qrcode order by hascontainer.location_qrcode"
            myresult = self.handleSQL(sql,True,None)
            temp = []
            for result in myresult[1]:
                temp.append({"email":result[0],"qrcode":result[1],"statusUpdateTime":str(result[2]),"location_qrcode":result[3]})
            return True, temp
        except Exception as e:
            logging.error("Error in totalContainersInBins")
            logging.error(str(e))
            return self.handleError(e)

    def totalContainersInStock(self):
        try:
            logging.info("Entering totalContainersInStock")
            sql = "select hascontainer.qrcode from hascontainer, location where hascontainer.status = 'Pending Return' and location.lastPickup > hascontainer.statusUpdateTime and location.location_qrcode = hascontainer.location_qrcode"
            sql1 = "SELECT container.qrcode FROM container LEFT JOIN hascontainer ON container.qrcode = hascontainer.qrcode WHERE hascontainer.qrcode IS NULL;"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            myresult1 = self.handleSQL(sql1,True,None)
            if(myresult1[0] == False):
                return myresult
            temp = []
            for result in myresult[1]:
                temp.append({"qrcode":result[0]})
            for result in myresult1[1]:
                temp.append({"qrcode":result[0]})
            return True, temp
        except Exception as e:
            logging.error("Error in totalContainersInStock")
            logging.error(str(e))
            return self.handleError(e)


    # CREATE CONTAINER
    def insertContainer(self,c):
        try:
            """
            myresult = self.checkFormatting(c)
            if(myresult[0] == False):
                return myresult
            """
            logging.info("Entering insertContainer")
            result = c.containerToList()
            sql = "INSERT INTO container (qrcode) VALUE (%s)"
            myresult = self.handleSQL(sql,False,result)
            if(myresult[0] == False):
                return myresult
            logging.info("insertContainer successful")
            return True, ""
        except Exception as e:
            logging.error("Error in insertContainer")
            logging.error(str(e))
            return self.handleError(e)

    #READ ALL CONTAINERS
    def selectAll(self): #returns --> "true, list of location objects"
        try:
            logging.info("Entering selectAll")
            sql = "SELECT * FROM container"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0]==False):
                return myresult
            result = []
            for row in myresult[1]:
                #container = Container(row[0],row[1],row[2])
                #result.append(container)
                container = Container(row[0])
                result.append(container)
            return True, result
        except Exception as e:
            logging.error("Error in selectAll")
            logging.error(str(e))
            return self.handleError(e)
    
    # READ CONTAINER
    def selectContainer(self,qrcode):
        try: 
            logging.info("Entering selectContainer")
            sql = "SELECT * FROM container WHERE qrcode = '" + qrcode + "'"
            myresult = self.handleSQL(sql,True,None)
            if(myresult[0] == False):
                return myresult
            logging.info("selectContainer successful")
            #myresult look like (True, [('101010',)])
            myresult2 = myresult[1][0][0]
            container = Container(myresult2)
            return True, container
        except Exception as e:
            logging.error("Error in selectContainer")
            logging.error(str(e))
            return self.handleError(e)

    # UPDATE CONTAINER
    def updateContainer(self,c):
        try:
            """
            myresult = self.checkFormatting(c)
            if(myresult[0] == False):
                return myresult
            """
            logging.info("Entering updateContainer")
            result = c.containerToList()
            sql = "UPDATE container WHERE qrcode = '" + result[0] + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("updateContainer successful")
            return True, ""
        except Exception as e:
            logging.error("Error in updateContainer")
            logging.error(str(e))
            return self.handleError(e)

    # DELETE CONTAINER
    def deleteContainer(self,c):
        try:
            """
            myresult = self.checkFormatting(c)
            if(myresult[0] == False):
                return myresult
            """
            logging.info("Entering deleteContainer")
            result = c.containerToList()
            sql = "DELETE FROM container WHERE qrcode = '" + result[0] + "'"
            myresult = self.handleSQL(sql,False,None)
            if(myresult[0] == False):
                return myresult
            logging.info("deleteContainer successful")
            return True, ""
        except Exception as e:
            logging.error("Error in deleteContainer")
            logging.error(str(e))
            return self.handleError(e)
#____________________________________________________________________________________________________________

    # CHECK FORMATTING
    def checkFormatting(self,c):
        myresult = self.checkLength(c)
        if myresult[0] == False:
            return myresult
        return True, ""
    
    def checkLength(self,c):
        maxLength = {
        "qrcode" : 45}
        var = "None"
        if(len(c.qrcode)>maxLength["qrcode"]):
            var = "qrcode"
        if(var == "None"):
            return True, ""
        else:
            temp = var + " is too long, maximum length: " + str(maxLength[var])
            return False, temp