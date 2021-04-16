# script to insert all QR Codes into the database tables

from container import Container
from containerDAO import ContainerDAO

from location import Location
from locationDAO import LocationDao

import mysql.connector
dao = ContainerDAO()
#dao2 = LocationDAO()

class insertQRcodes:
    def main():
        with open('containers.txt') as f:
            #print(f.read())
            for qrcode in f:
                c = Container(qrcode.rstrip("\n"))
                dao.insertContainer(c)
                print("successfully inserted", qrcode.rstrip("\n"))

        """
        with open('locations.txt') as f2:
            #print(f2.read())
            for qrcode in f2:
                l = Location(location_qrcode,description,lastPickup,containers)
                dao2.insertLocation(l)
                print("successfully inserted", location_qrcode.rstrip("\n"))
        """
    main()