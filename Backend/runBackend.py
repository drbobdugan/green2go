from flask import Flask
import mysql.connector
import json
from flask import request
app = Flask(__name__)

mydb = mysql.connector.connect(
        host="198.199.77.174",
        user="root",
        password="Capstone2021!",
        database="sys")


@app.route('/getTables', methods=['GET', 'POST'])
def hello_world():

    print(request.json["value"])

    global mydb

    mycursor = None
    # try to see if connection is alive
    try:
        mycursor = mydb.cursor()
    except:
        # try to reconnect if broken cnnxn
        mydb = mysql.connector.connect(
        host="198.199.77.174",
        user="root",
        password="Capstone2021!",
        database="sys")
        mycursor = mydb.cursor()
    # execute command
    mycursor.execute("SHOW TABLES")
    # empty list to return items
    out = []
    d = {}
    # add things to empty list
    for x in mycursor:
        out.append(x[0])
    #return list as json
    d["data"] = out
    return json.dumps(d)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')