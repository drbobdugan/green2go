from flask import Flask
import mysql.connector
import json
from flask import request
from userDao import UserDao
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
@app.route('/addUser', methods=['POST'])
def addUser():
    if request.method =='POST':
        newuser=[request.form['email'], request.form['password'], request.form['firstName'],request.form['lastName'], request.form['middleName'], request.form['phoneNum'], request.form['role'], request.form['classYear'], request.form['authCode'],request.form['authTime'],request.form['lastLogIn']]
        dao=UserDao()
        dao.addUser(newuser)
@app.route('/updateUser', methods=['GET','POST'])
def updateUser():
       dao=UserDao()
       user=dao.getUser(request.form['email']) # how put in the connect to app where the email is coming from
       userupdate=[user.email, user.password, user.firstName,user.lastName, user.middleName, user.phoneNum, user.role, user.classYear, user.authCode,user.authTime,user.lastLogIn]
       dao.updateUser(userupdate)

@app.route('/deleteUser', methods=['GET','POST'])
def deleteUser():
    dao=UserDao()
    user=dao.getUser(request.form['email'])# get the value from the frontend for the Email
    dao.deleteUser(user)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')