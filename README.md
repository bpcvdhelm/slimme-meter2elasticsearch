# slimme-meter2elasticsearch
## Hardware setup
I've implemented a Pi Zero connected to an ISKRA meter type AM550-TD2.01. It is just a Pi Zero W with housing, a 16Gb microSD, an adapter, a "Slimme meter" cable and a USB cable micro-USB tto USB-A female.

## Implementation
Cron is running a script sm-check.sh every minute on the Pi Zero W. It has the simple task of starting the python script sm.py if it is not running.

### sm
The sm (Slimme meter, what else ;-) example is just the cron setting for starting up the sm.py script. Do not forget to load it into cron with the command (under root) service cron reload. This should start the whole thing up.

### sm.py
The python script will start reading from the slimme meter. It will pull out the telegrams every second. When the CRC is correct statistics will be kept for 5 minutes. On every 5 minute interval (based on the time the slimme meter provides) 2 jsons are added to a zipped _bulk elasticsearch file named <year>.<month>.gz. Example "2019.01.gz".

The reported fields are:
  - "CreateTimestamp": - "2019-01-04T07:34:58Z"
  - "GasTake.m3.avg": 818.05
  - "GasTake.m3.max": 818.051
  - "GasTake.m3.min": 817.985
  - "GasTake.m3.use": 0.066
  - "GasTimestamp.max": - "190104083002+0100"
  - "GasTimestamp.min": - "190104082509+0100"
  - "Measurements": 300
  - "Pwr.A.avg": 0.089
  - "Pwr.A.max": 6
  - "Pwr.A.min": 0
  - "Pwr.V.avg": 231.395
  - "Pwr.V.max": 235.2
  - "Pwr.V.min": 225.7
  - "Pwr.kWh.use": 0.039
  - "PwrGive.kW.avg": 0
  - "PwrGive.kW.max": 0
  - "PwrGive.kW.min": 0
  - "PwrL1.A.avg": 0.247
  - "PwrL1.A.max": 1
  - "PwrL1.A.min": 0
  - "PwrL1.V.avg": 227.879
  - "PwrL1.V.max": 229.5
  - "PwrL1.V.min": 225.7
  - "PwrL1Give.kW.avg": 0
  - "PwrL1Give.kW.max": 0
  - "PwrL1Give.kW.min": 0
  - "PwrL1Take.kW.avg": 0.147
  - "PwrL1Take.kW.max": 0.196
  - "PwrL1Take.kW.min": 0.119
  - "PwrL2.A.avg": 0.02
  - "PwrL2.A.max": 6
  - "PwrL2.A.min": 0
  - "PwrL2.V.avg": 232.341
  - "PwrL2.V.max": 233.8
  - "PwrL2.V.min": 230.8
  - "PwrL2Give.kW.avg": 0
  - "PwrL2Give.kW.max": 0
  - "PwrL2Give.kW.min": 0
  - "PwrL2Take.kW.avg": 0.157
  - "PwrL2Take.kW.max": 1.547
  - "PwrL2Take.kW.min": 0.149
  - "PwrL3.A.avg": 0
  - "PwrL3.A.max": 0
  - "PwrL3.A.min": 0
  - "PwrL3.V.avg": 233.965
  - "PwrL3.V.max": 235.2
  - "PwrL3.V.min": 232.4
  - "PwrL3Give.kW.avg": 0
  - "PwrL3Give.kW.max": 0
  - "PwrL3Give.kW.min": 0
  - "PwrL3Take.kW.avg": 0.164
  - "PwrL3Take.kW.max": 0.187
  - "PwrL3Take.kW.min": 0.081
  - "PwrT1.kWh.use": 0
  - "PwrT1Give.kWh.avg": 176.914
  - "PwrT1Give.kWh.max": 176.914
  - "PwrT1Give.kWh.min": 176.914
  - "PwrT1Give.kWh.use": 0
  - "PwrT1Take.kWh.avg": 828.427
  - "PwrT1Take.kWh.max": 828.427
  - "PwrT1Take.kWh.min": 828.427
  - "PwrT1Take.kWh.use": 0
  - "PwrT2.kWh.use": 0.039
  - "PwrT2Give.kWh.avg": 471.621
  - "PwrT2Give.kWh.max": 471.621
  - "PwrT2Give.kWh.min": 471.621
  - "PwrT2Give.kWh.use": 0
  - "PwrT2Take.kWh.avg": 409.028
  - "PwrT2Take.kWh.max": 409.047
  - "PwrT2Take.kWh.min": 409.008
  - "PwrT2Take.kWh.use": 0.039
  - "PwrTake.kW.avg": 0.47
  - "PwrTake.kW.max": 1.897
  - "PwrTake.kW.min": 0.357
  - "PwrTariff.avg": 2
  - "PwrTariff.max": 2
  - "PwrTariff.min": 2
  - "Timestamp.max": - "190104083459+0100"
  - "Timestamp.min": - "190104083000+0100"

