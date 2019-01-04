# slimme-meter2elasticsearch
## Hardware setup
I've implemented a Pi Zero connected to an ISKRA meter type AM550-TD2.01. It is just a Pi Zero W with housing, a 16Gb microSD, an adapter, a "Slimme meter" cable and a USB cable micro-USB tto USB-A female.

## Implementation
Cron is running a script sm-check.sh every minute on the Pi Zero W. It has the simple task of starting the python script sm.py if it is not running.

### sm
The sm (Slimme meter, what else ;-) example is just the cron setting for starting up the sm.py script. Do not forget to load it into cron with the command (under root) service cron reload. This should start the whole thing up.

### sm.py
The python script will start reading from the slimme meter. It will pull out the telegrams every second. When the CRC is correct statistics will be kept for 5 minutes. On every 5 minute interval (based on the time the slimme meter provides) 2 jsons are added to a zipped _bulk elasticsearch file named <year>.<month>.gz. Example "2019.01.gz".

Here is an example output:

{"index":{"_index":"sm-2019.01","_type":"doc","_id":"2019-01-04T07:14:59Z"}}
{"PwrL1.A.avg":0.22,"PwrL1.A.min":0.0,"PwrL3.A.avg":0.0,"Pwr.A.min":0.0,"PwrL3.V.min":233.2,"PwrL2.V.min":230.7,"PwrL1.V.avg":231.602,"GasTake.m3.min":817.74,"Measurements":300,"PwrTariff.min":2,"PwrT1Give.kWh.avg":176.914,"PwrT1Give.kWh.use":0.0,"PwrT1Give.kWh.min":176.914,"PwrL1.A.max":1.0,"GasTimestamp.min":"190104080508+0100","PwrL2Give.kW.min":0.0,"PwrT2Take.kWh.min":408.873,"PwrL2.V.avg":232.744,"PwrGive.kW.max":0.0,"PwrL1Give.kW.avg":0.0,"PwrT2Give.kWh.max":471.621,"PwrT1Give.kWh.max":176.914,"PwrTariff.avg":2.0,"PwrL1Take.kW.min":0.12,"PwrT1.kWh.use":0.0,"PwrL3.V.avg":234.399,"GasTake.m3.max":817.798,"PwrL3Give.kW.avg":0.0,"PwrT2.kWh.use":0.033,"PwrT1Take.kWh.use":0.0,"PwrL1Take.kW.max":0.189,"Pwr.V.max":235.6,"PwrL1.V.max":232.9,"PwrTake.kW.max":1.789,"PwrL3Take.kW.avg":0.083,"PwrL3Take.kW.min":0.081,"PwrL1.V.min":229.9,"PwrT2Take.kWh.max":408.906,"PwrTake.kW.avg":0.397,"CreateTimestamp":"2019-01-04T07:14:59Z","PwrTariff.max":2,"GasTimestamp.max":"190104081008+0100","PwrTake.kW.min":0.363,"PwrL2Take.kW.max":1.549,"Pwr.V.avg":232.915,"GasTake.m3.use":0.058,"PwrL2Take.kW.avg":0.169,"PwrL3Give.kW.max":0.0,"Pwr.kWh.use":0.033,"PwrT2Give.kWh.use":0.0,"PwrL1Give.kW.max":0.0,"Pwr.A.max":6.0,"PwrL3.V.max":235.6,"PwrT2Give.kWh.avg":471.621,"PwrT2Give.kWh.min":471.621,"Timestamp.min":"190104081000+0100","PwrL3.A.max":0.0,"PwrGive.kW.min":0.0,"PwrT2Take.kWh.use":0.033,"PwrL2.A.min":0.0,"PwrGive.kW.avg":0.0,"PwrL2Give.kW.max":0.0,"PwrL2.A.avg":0.02,"PwrT1Take.kWh.avg":828.427,"Pwr.V.min":229.9,"Pwr.A.avg":0.08,"PwrT1Take.kWh.min":828.427,"PwrL2.V.max":233.7,"PwrL2Give.kW.avg":0.0,"Timestamp.max":"190104081459+0100","PwrT1Take.kWh.max":828.427,"PwrT2Take.kWh.avg":408.889,"GasTake.m3.avg":817.796,"PwrL1Give.kW.min":0.0,"PwrL1Take.kW.avg":0.144,"PwrL3.A.min":0.0,"PwrL3Give.kW.min":0.0,"PwrL3Take.kW.max":0.09,"PwrL2Take.kW.min":0.157,"PwrL2.A.max":6.0}
