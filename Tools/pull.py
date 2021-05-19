from flask import Flask, request
import os
import sys
import subprocess
import requests
from pathlib import Path
sys.path.insert(0, os.getcwd())
app = Flask(__name__)



@app.route('/pull', methods=['POST'])
def hello(msg="Build has been Updated..."):
    test = os.system('cd /root/green2go/Tools/ && ./startBackend.sh')
    os.system('cd /root/green2go/Tools/ && nohup ./startWeb.sh &')
    url = 'https://hooks.slack.com/services/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'
    myobj = {'text': msg}
    x = requests.post(url, json = myobj)
    return str(x.text)

def restartDatabase():
    os.system('sudo service mysql restart')
    url = 'https://hooks.slack.com/services/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'
    myobj = {'text' : 'Databse Restarted'}
    x = requests.post(url, json = myobj)
    return str(x.text)

def deleteUser(email):
    url = "http://198.199.77.174:5000/secretDeleteUser"
    myobj = {'email': email}
    x = requests.delete(url, json=myobj) 
    print(x.text)

@app.route('/deleteUser', methods=['GET', 'POST'])
def renderDelete():
    configData = initializeConfigInfo()

    if 'password' in request.form and 'email'in request.form and request.form['password'] == configData['password']:
        deleteUser(request.form['email'].replace(' ', '').replace('\n', ''))
    return """<!doctype html>
    <html>
    <body>
    <form method='POST'>
    <h2> Delete User </h2>
    <h1> Email </h1>
    <input type="text" name="email">
    <h1> Confirm (Not Email Password...) </h1>
    <input type="text" name="password">
    <br/>
    <input type="submit">
    </form>
    </body>
    </html>
    """

def updateCheckout():
    url = "http://198.199.77.174:5000/secretGetRelationships?email=Checkout@stonehill.edu"
    x = requests.get(url)
    return x.json()

@app.route('/checkout', methods=['GET', 'POST'])
def checkoutByEmail():
    configData = initializeConfigInfo()
    if 'password' in request.form and 'email' in request.form and request.form['password'] == configData['password']:
        url = "http://198.199.77.174:5000/secretCheckout"
        myobj = {'email' : request.form['email']}
        x = requests.post(url, json=myobj)
    userContainers = updateCheckout()
    dataBody = ""
    for item in userContainers['data']:
        dataBody = dataBody + (item['qrcode']+" : "+item['status']+"<br>")
    return """<!doctype html>
    <html>
    <body>
    <form method='POST'>
    <h2> Checkout Container </h2>
    <h1> Email </h1>
    <input type="text" name="email">
    <h1>Confirm (Not Email Password...) </h1>
    <input type="text" name="password">
    <br/>
    <input type="submit">
    <h2> Checkout Log </h2>
    """ +dataBody+ """
    </form>
    </body>
    </html>
    """

def getVersion(host):
    url="http://198.199.77.174:5000/getVersion?host="+host
    x = requests.get(url)
    return x.json()

def updateVersion(version):
    url="http://198.199.77.174:5000/update"+version
    myobj = {'host' : 'iOS'}
    x = requests.post(url, json=myobj)
    myobj = {'host' : 'Android'}
    x = requests.post(url, json=myobj)


@app.route('/version', methods=['GET', 'POST'])
def version():
    if "update" in request.form and request.form['update'] != " ":
        updateVersion(request.form['update'])
    apple = getVersion('iOS')
    apple = apple['data']
    android = getVersion('Android')
    android = android['data']
    return """<!doctype html>
    <html>
    <body>
    <form method='POST'>
    <h1> Current versions <h1>
    <h3> iOS : """ + apple + """ </h3>
    <h3> Android : """ + android + """ </h3>
    <h2> Update Version </h2>
    <label for="update"> Choose an update: </label>
    <select name="update" id="update">
    <option value=" "></option>
    <option value="Major">Major</option>
    <option value="Minor">Minor</option>
    <option value="Patch">Patch</option>
    </select>
    <br><br>
    <input type="submit">
    </form>
    </body>
    </html>
    """

@app.route('/server', methods=['GET', 'POST'])
def control():
    configData = initializeConfigInfo()
    status = os.popen('lsof -i:5000 -t').read()
    val = None
    f = open('/root/green2go/Backend/demo.log')
    lines = f.readlines()
    linesTemp = ""
    for line in lines:
        linesTemp = linesTemp + "<p>" + line + "</p>"
    f.close()
    if status.find('\n') != -1 or (status != "" and int(status) > 0):
        val = "Online"
    else:
        val = "Offline"
    if 'Password' in request.form and request.form['Password'] == configData['password']:
        hello("Server has been restarted...")
    if 'Password1' in request.form and request.form['Password1'] == configData['password']:
        restartDatabase()
    return """<!doctype html>
    <html>
    <body>
    <h1>"""+ str(val)  + """ </h1>
    <h3> Restart Server </h3>
    <form method='POST'>
    <input type="text" name="Password">
    <input type="submit">
    </form>
    <h3> Restart Databse </h3>
    <form method='POST'>
    <input type="text" name="Password1">
    <input type="submit">
    </form>
    <h3> Log File </h3>
    """+ str(linesTemp) + """
    </body>
    </html>"""



def initializeConfigInfo():
    configData = {} 
    path = os.path.abspath('/root/credentials.txt')
    with open(path) as file:
        for line in file:
            (key,value) = line.split()
            configData[key] = value
    file.close()

    return configData
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
