import logging
FORMAT = "[%(asctime)s%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
logging.basicConfig(filename='output.log',format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
import mysql.connector
import json
import dataset
from datetime import datetime
from DAO import dao
from location import Location

class LocationDao:

    def rowToLocation(self,row):
        location = Location(row['location_qrcode'], row['description'], row['lastPickup'])
        return location

    def locationToRow(self,location):
        row = dict(location_qrcode=location.location_qrcode, description=location.description,lastPickup=location.lastPickup)
        return row

    def selectAll(self):
        table = self.mydb['location']
        rows   = table.all()

        result = []
        for row in rows:
            result.append(self.rowToLocation(row))
        return result
    
    def selectByLocationQRcode(self,location_qrcode):
        row = self.table.find_one(location_qrcode=location_qrcode)

        result = None
        if (row is None):
            logger.error('Failed to find location with ' + location_qrcode)
        else:
            result = self.rowToLocation(row)
        return result
        
    def insert(self,location):
        self.table.insert(self.locationToRow(location))
        self.mydb.commit()

    def update(self,location):
        self.table.update(self.locationToRow(location),['location_qrcode'])
        self.mydb.commit()

    def delete(self,location):
        self.table.delete(location_qrcode=location_qrcode)
        self.mydb.commit()