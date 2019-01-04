# slimme-meter2elasticsearch
## Hardware setup
I've implemented a Pi Zero connected to an ISKRA meter type AM550-TD2.01. It is just a Pi Zero W with housing, a 16Gb microSD, an adapter, a "Slimme meter" cable and a USB cable micro-USB tto USB-A female.

## Implementation
Cron is running a script sm-check.sh every minute on the Pi Zero W. It has the simple task of starting the python script sm.py if it is not running.

### sm
The sm (Slimme meter, what else ;-) example is just the cron setting for starting up the sm.py script. Do not forget to load it into cron with the command (under root) service cron reload. This should start the whole thing up.

### sm.py
The python script will start reading from the slimme meter. It will pull out the telegrams every second. When the CRC is correct statistics will be kept for 5 minutes. On every 5 minute interval (based on the time the slimme meter provides) 2 jsons are added to a zipped _bulk elasticsearch file named <year>.<month>.gz. Example "2019.01.gz".
