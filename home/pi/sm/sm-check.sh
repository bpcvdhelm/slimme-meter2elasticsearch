#!/bin/bash
#exit

Logfilename="/home/pi/sm/log/sm.log"
Pythonname="/home/pi/sm/sm.py"
Scriptname="/home/pi/sm/sm.sh"

#------------------------------------------------------------------------------#
# Start the sm.py script when it is not running                                #
#------------------------------------------------------------------------------#
Running=$(ps -ef  | grep sm | grep python | wc -l)
if [ $Running -ne 1 ]; then
  echo $(date) $Scriptname "Starting python script" $Pythonname >> $Logfilename
  python $Pythonname >> $Logfilename 2>&1
  echo $(date) $Scriptname "Script" $Pythonname "ended" >> $Logfilename
fi
