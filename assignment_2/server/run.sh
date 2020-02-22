
rm rover.db
sqlite3 rover.db < query.sql
echo "IP: 127.0.0.1   PORT: 9002"
./rover_net 127.0.0.1:9002 level.json 2> /dev/null > /dev/null
