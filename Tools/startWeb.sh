sudo kill -9 $( lsof -i:5002 -t)
cd /root/green2go/Frontend/Web/choose2reuse
npm i
nohup npm start &
