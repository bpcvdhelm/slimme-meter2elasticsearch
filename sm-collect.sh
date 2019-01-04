scp pi@zerosm:/home/pi/sm/json/sm-*.*.gz /home/bernard/sm/json
zcat /home/bernard/sm/json/sm-*.*.gz | curl -k -XPOST "localhost:9200/_bulk" -H "Content-Type:application/x-ndjson" --data-binary @-
