from flask import Flask, request
import os
import subprocess
import requests
app = Flask(__name__)


@app.route('/pull', methods=['POST'])
def hello(msg="Build has been Updated..."):
    os.system('sudo kill -9 $( lsof -i:5000 -t)')
    os.system('cd /root/green2go/ && git pull')
    os.system('cd /root/green2go/Backend && rm demo.log')
    test = os.system('cd /root/green2go/Backend/ && sudo NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program nohup python3 /root/green2go/Backend/runBackend.py &')
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
    if 'password' in request.form and 'email'in request.form and request.form['password'] == 'Capstone2021!':
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
    url = "http://198.199.77.174:5000/secretGetRelationships"
    myobj = {'email' : 'Checkout@stonehill.edu'}
    x = requests.get(url, json=myobj)
    return x.text

@app.route('/checkout', methods=['GET', 'POST'])
def checkoutByEmail():
    if 'password' in request.form and 'email' in request.form and request.form['password'] == 'Capstone2021!':
        url = "http://198.199.77.174:5000/secretCheckout"
        myobj = {'email' : request.form['email']}
        x = requests.post(url, json=myobj)
    print(userContainers)
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
    """ +userContainers+ """
    </form>
    </body>
    </html>
    """

@app.route('/server', methods=['GET', 'POST'])
def control():
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
    if 'Password' in request.form and request.form['Password'] == 'Capstone2021!':
        hello("Server has been restarted...")
    if 'Password1' in request.form and request.form['Password1'] == 'Capstone2021!':
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
