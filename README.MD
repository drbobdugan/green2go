# choose2reuse

This project was created by the Stonehill College 2020-21 Spring C.S. capstone. It contains the full-stack for the choose2reuse application.

## Table of Contents
1. [Project Dependancies](#depend)
2. [Project Installation](#install)
3. [Database Installation](#db)
4. [Back-End Installation](#back)
5. [Front-End Installation](#front)
6. [Web App Installation](#web)
7. [Testing](#test)
8. [Tools](#tools)
9. [How is The Stack Currently Implemented?](#stack)
10. [Database Tables and DAO Information](#databaseInfo)
11. [Contributors](#contribs)
12. [ToDo](#todo)
13. [Additional Information](#additional)

## Project Dependancies <a name="depend"></a>
- Android Studio
  - https://developer.android.com/studio
- dart
  - https://dart.dev/get-dart
- flutter
  - https://flutter.dev/docs/get-started/install
- git
  - https://git-scm.com/downloads
- New Relic (optional)
  - https://docs.newrelic.com/docs/using-new-relic/cross-product-functions/install-configure/install-new-relic/
- nodejs
  - https://nodejs.org/en/download/
- npm
  - https://www.npmjs.com/get-npm
- pip3
  - https://pypi.org/project/pip/
- python3
  - https://www.python.org/downloads/
- vscode (optional)
  - https://code.visualstudio.com/

## Project Installation <a name="install"></a>

To install:
```bash
git clone https://github.com/drbobdugan/green2go.git
cd green2go
```


Result: Project folder is cloned to current working directory

## Database Installation <a name="db"></a>

```bash
# download and install mysql installer on ubuntu
sudo apt install mysql-server
# run mysql installation
# Note: to keep this working with stack make sure its on port 3306
sudo mysql_secure_installation
```

Result: Sets up database

## Back-End Installation (python3/flask) <a name="back"></a>
Contact a user to get an environmentVars.py file which contains variables this project will need to run. Additionally make these changes to run the Backend locally:

#app.run(host='0.0.0.0', port='5000', ssl_context=context)#ssl context for https

app.run(host='0.0.0.0', port='5000')

To install/run:
```bash
cd Backend
pip3 install -r requirements.txt
python3 runBackend.py
```

Result: Runs flask server on port 5000 in terminal

## Web App Installation (nodejs/react) <a name="web"></a>

To install/run:
```bash
cd Frontend/Web/choose2reuse
npm i
npm start
```

Result: Opens browser to a new tab at localhost:3000 where the web server is running


## Front-End Installation (flutter) <a name="front"></a>

To install/run:
```bash
cd Frontend/choose2reuse
flutter doctor
flutter run
```

Result: Opens testing/non-production build on an emulator

## Testing <a name="test"></a>


Testing schedule: https://docs.google.com/spreadsheets/d/1pLRcGYRma7AQFMuWo2ZMpMzEH3oFvBu0_HslGrhkKto/edit#gid=0 <br/>
<br/>
Insert more testing info here... <br/>

## Tools <a name="tools"></a>

RELEASE ANDROID BETA BUILDS FOR TESTING:
- IN REPOSITORY:
- In the “pubspec.yaml” file within “Frontend/choose2reuse/“, find the line “version:  1.0.0+0” and increment build/version each time you build  (increment the values in position X)->   version:  1.0.X+X

- IN TERMINAL:
- Run these commands in the ‘Frontend/choose2reuse/‘ directory:
    - flutter clean 
    -  flutter build appbundle

- IN ANDROID PLAY CONSOLE:
- Sign in using CapstoneSpring2021@gmail.com
- Go to “All Apps” and click the “GreenZGo” app
- Click on the Testing -> Internal testing tab
- Click “Create new release”
- Click “upload appbundle”, and select the file “app-release.aab” from “Frontend/choose2reuse/build/app/outputs/bundle/ “
- Once the file loads, scroll to the bottom and click “save”
- Click “Rollout to internal testers”



DATABASE BACKUPS:
- The “sys” database is being backed up every morning at 3:00am by a command running on the server in “/etc/crontab”
- The command is: 
"0 3 * * * root mysqldump -u root -p"put database password here" sys > ../../mysql_backup/backup_$(date +\%Y\%m\%d\%H\%M).sql"
- The backups are saved to the “/mysql_backups” directory, and are called “backup_{YYYY-MM-DD}.sql
- To restore the database, you must create an empty database and copy the backup into it. 
- This can be done with the command: "mysql -u root -p newDatabase < /mysql_backups/{whatever file you want}.sql"


TRAVIS-CI:
- Go to travis-ci.org, and Sign in using Drbobdugan@gmail.com (the project GitHub account)
- Select the repository you want to use (drbobdugan/green2go), and watch the progress of unit tests being performed in real time
- Travis works by executing commands specified in the ".travis.yml" file in the root of the project.
- You can learn how to use it here: https://docs.travis-ci.com/



## How is The Stack Currently Implemented? <a name="stack"></a>

Currently, the server we are using is an ubuntu instance hosted on a droplet at digitalocean, a hosting site. <br/>

Open Ports (That I'm aware of): <br/>
- 5000 (flask)
- 5001 (tools)
- 22 (ssh)
- 3306 (mysql)

Make sure the ubuntu vm stays up to date for security reasons:
```bash
# download updates
sudo apt update
# install updates (moat likely need to agree)
sudo apt upgrade
```

<br/>
The mysql server is running as a service:

```bash
# to start
sudo service mysql start
# to stop
sudo service mysql stop
# to restart
sudo service mysql restart
```

The flask server is running as two processes (One logging and the other handling):

```bash
# to check if the server is running/list pids
lsof -i:5000 -t
# to kill the server and all instances based on port
kill -9 $(lsof -i:5000 -t)
# to start the backend and leave it running when you disconnect
cd Backend
# start server (w/o new relic)
nohup python3 runBackend.py &
  or
# start with new relic
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program nohup python3 /root/green2go/Backend/runBackend.py &
```

Automatic updates to backend/web app and slack alerts:<br/>
There is a file called pull.py currently located in /Tools/ that controls slack alerts and controls anything on port 5001.
```bash
# to check if the server is running/list pids
lsof -i:5001 -t
# to kill the server and all instances based on port
kill -9 $(lsof -i:5001 -t)
# to start
cd /Tools/
nohup python3 pull.py &
```

## Database Tables and DAO Information <a name="databaseInfo"></a>

Each table in the database as a corresponding object, DAO (data access object), and unit test. These tables include location, container, hascontainer (relationship), user, and auth. To view the fields of each table, you can check MySQL or the .py file for the object. Each DAO contains methods which create, read, update and delete (CRUD) from the database. Make sure to run the corresponding unit test each time you make a change to the DAO and object. The unit test will write all errors to the DAO.log file for debugging purposes.


## Contributors <a name="contribs"></a>
- Pat O'Shea
- Ethan Batt
- Shawn LaBonte
- Luciano Giannini
- Bob Dugan
- Ruthie Missett
- Samantha Salvas
- Andrew Petti
- Elizabeth Blake
- Parker Rowley
- Marianne Kenney
- Taylor Li
- Aaron Jones
- Dylan Vieira
- Thomas Hines
- Mike Sale
- Caleb Hadley

## TO DO: <a name="todo"></a>

- [X] Begin updating documentation
- [X] Make everyone aware of Documentation and ask them to update it
- [ ] Make sure all dependencies are listed
- [X] Add database setup to documentation along with sql files to create database
- [ ] Add testing info to documentation
- [ ] Add tools info to documentation
- [ ] Have someone test installation flow
- [ ] Finalize documentation
- [ ] Make Project Private

## Additional Info. <a name="additional"></a>
Server ip: 198.199.77.174 <br/>
Follow progress at: https://www.pivotaltracker.com/n/projects/2487958 <br/>
Server logs: http://198.199.77.174:5001/server <br/>
Restart Backend: http://198.199.77.174:5001/server <br/>
Restart Database: http://198.199.77.174:5001/server <br/>
Password File: Ask a contributor <br/>
New Relic: https://one.newrelic.com/ <br/>
Code Climate: https://codeclimate.com/github/drbobdugan/green2go/ <br/>
