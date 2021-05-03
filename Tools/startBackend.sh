sudo kill -9 $( lsof -i:5000 -t)
cd /root/green2go/ && git pull
cd /root/green2go/Backend && rm demo.log
cd /root/green2go/Backend/ && sudo NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program nohup python3 /root/green2go/Backend/runBackend.py &
