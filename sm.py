import datetime
import gzip
import json
import serial

#------------------------------------------------------------------------------#
# Constants                                                                    #
#------------------------------------------------------------------------------#
JsonDir = "/home/pi/sm/json/"
SerialPort = "/dev/ttyUSB0"

#------------------------------------------------------------------------------#
# Setup serial line to "Slimme" meter                                          #
#------------------------------------------------------------------------------#
def SetupSerialLine():
  SerialLine = serial.Serial()
  SerialLine.baudrate = 115200
  SerialLine.bytesize = serial.EIGHTBITS
  SerialLine.parity = serial.PARITY_NONE
  SerialLine.port = SerialPort
  SerialLine.stopbits = serial.STOPBITS_ONE
  SerialLine.timeout = 2
  SerialLine.open()
  return SerialLine

#------------------------------------------------------------------------------#
# Calculate the Telegram CRC16                                                 #
#------------------------------------------------------------------------------#
def CRC16(Telegram):
  CRC = 0x0000
  for Line in Telegram:
    for Char in Line:
      CRC ^= 0x00ff & ord(Char)
      for _ in range(0, 8):
        if (CRC & 0x0001):
          CRC >>= 1
          CRC ^= 0xa001
        else:
          CRC >>= 1
  return CRC

#------------------------------------------------------------------------------#
# Read in a whole telegram and return the lines in a list                      #
#------------------------------------------------------------------------------#
def ReadTelegram(SerialLine):
  Header = False
  Footer = False
  Telegram = []
  while Footer == False:
    Line = SerialLine.readline()
    if Header == True:
      Telegram.append(Line)
      if Line[0] == '!':
        Footer = True
    elif Line[0] == '/':
      Header = True
      Telegram.append(Line)
  return Telegram

#------------------------------------------------------------------------------#
# Convert Telegram lines to Dictionary                                         #
#------------------------------------------------------------------------------#
def Telegram2Dict(Telegram):
  Dict = {}
  for Line in Telegram[2:-1]:
    Key = ''
    Value = ''
    ValueFound = False
    for Char in Line[:-2]:
      if Char == '(':
        ValueFound = True
      if ValueFound == True:
        Value += Char
      else:
        Key += Char
    Dict[Key] = Value
  return Dict

#------------------------------------------------------------------------------#
# Interpret the Telegram findings                                              #
#------------------------------------------------------------------------------#
def InterpretDict(Dict):
  SecStats = {}
  SecStats['GasTake.m3'] = float(Dict['0-1:24.2.1'][16:-4])
  SecStats['GasTimestamp'] = Dict['0-1:24.2.1'][1:-15]
  if SecStats['GasTimestamp'][-1] == 'S':
    SecStats['GasTimestamp'] = SecStats['GasTimestamp'][:-1] + "+0200"
  else:
    SecStats['GasTimestamp'] = SecStats['GasTimestamp'][:-1] + "+0100"
  SecStats['PwrGive.kW'] = float(Dict['1-0:2.7.0'][1:-4])
  SecStats['PwrL1.A'] = float(Dict['1-0:31.7.0'][1:-3])
  SecStats['PwrL1.V'] = float(Dict['1-0:32.7.0'][1:-3])
  SecStats['PwrL1Give.kW'] = float(Dict['1-0:22.7.0'][1:-4])
  SecStats['PwrL1Take.kW'] = float(Dict['1-0:21.7.0'][1:-4])
  SecStats['PwrL2.A'] = float(Dict['1-0:51.7.0'][1:-3])
  SecStats['PwrL2.V'] = float(Dict['1-0:52.7.0'][1:-3])
  SecStats['PwrL2Give.kW'] = float(Dict['1-0:42.7.0'][1:-4])
  SecStats['PwrL2Take.kW'] = float(Dict['1-0:41.7.0'][1:-4])
  SecStats['PwrL3.A'] = float(Dict['1-0:71.7.0'][1:-3])
  SecStats['PwrL3.V'] = float(Dict['1-0:72.7.0'][1:-3])
  SecStats['PwrL3Give.kW'] = float(Dict['1-0:62.7.0'][1:-4])
  SecStats['PwrL3Take.kW'] = float(Dict['1-0:61.7.0'][1:-4])
  SecStats['PwrTake.kW'] = float(Dict['1-0:1.7.0'][1:-4])
  SecStats['PwrTariff'] = int(Dict['0-0:96.14.0'][1:-1])
  SecStats['PwrT1Give.kWh'] = float(Dict['1-0:2.8.1'][1:-5])
  SecStats['PwrT1Take.kWh'] = float(Dict['1-0:1.8.1'][1:-5])
  SecStats['PwrT2Give.kWh'] = float(Dict['1-0:2.8.2'][1:-5])
  SecStats['PwrT2Take.kWh'] = float(Dict['1-0:1.8.2'][1:-5])
  SecStats['Timestamp'] = Dict['0-0:1.0.0'][1:-1]
  if SecStats['Timestamp'][-1] == 'S':
    SecStats['Timestamp'] = SecStats['Timestamp'][:-1] + "+0200"
  else:
    SecStats['Timestamp'] = SecStats['Timestamp'][:-1] + "+0100"
  return SecStats

#------------------------------------------------------------------------------#
# Perform statistics                                                           #
#------------------------------------------------------------------------------#
def Statistics(SecStats, Min, Max, Avg):
  try:
    Avg['Measurements'] += 1
    for Key in SecStats:
      if not isinstance(SecStats[Key], basestring):
        Avg[Key] = round(Avg[Key] + SecStats[Key], 3)
      if Max[Key] < SecStats[Key]:
        Max[Key] = SecStats[Key]
      if Min[Key] > SecStats[Key]:
        Min[Key] = SecStats[Key]
  except:
    Avg['Measurements'] = 1
    for Key in SecStats:
      if not isinstance(SecStats[Key], basestring):
        Avg[Key] = SecStats[Key]
      Max[Key] = SecStats[Key]
      Min[Key] = SecStats[Key]

#------------------------------------------------------------------------------#
# Output a Json with the Stats                                                 #
#------------------------------------------------------------------------------#
def Stats2Json(Min, Max, Avg):
  Json = {}
  Measurements = Avg.pop('Measurements')
  for Key in Avg:
    Json[Key + '.avg'] = round(Avg[Key] / Measurements, 3)
  for Key in Max:
    Json[Key + '.max'] = Max[Key]
  for Key in Min:
    Json[Key + '.min'] = Min[Key]
  Json['CreateTimestamp'] = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
  Json['GasTake.m3.use'] = round(Json['GasTake.m3.max'] - Json['GasTake.m3.min'], 3)
  Json['Measurements'] = Measurements
  Json['Pwr.A.avg'] = round((Json['PwrL1.A.avg'] + Json['PwrL2.A.avg'] + Json['PwrL3.A.avg']) / 3, 3)
  Json['Pwr.A.max'] = max(Json['PwrL1.A.max'], Json['PwrL2.A.max'], Json['PwrL3.A.max'])
  Json['Pwr.A.min'] = min(Json['PwrL1.A.min'], Json['PwrL2.A.min'], Json['PwrL3.A.min'])
  Json['Pwr.V.avg'] = round((Json['PwrL1.V.avg'] + Json['PwrL2.V.avg'] + Json['PwrL3.V.avg']) / 3, 3)
  Json['Pwr.V.max'] = max(Json['PwrL1.V.max'], Json['PwrL2.V.max'], Json['PwrL3.V.max'])
  Json['Pwr.V.min'] = min(Json['PwrL1.V.min'], Json['PwrL2.V.min'], Json['PwrL3.V.min'])
  Json['PwrT1Give.kWh.use'] = round(Json['PwrT1Give.kWh.max'] - Json['PwrT1Give.kWh.min'], 3)
  Json['PwrT1Take.kWh.use'] = round(Json['PwrT1Take.kWh.max'] - Json['PwrT1Take.kWh.min'], 3)
  Json['PwrT1.kWh.use'] = round(Json['PwrT1Take.kWh.use'] - Json['PwrT1Give.kWh.use'], 3)
  Json['PwrT2Give.kWh.use'] = round(Json['PwrT2Give.kWh.max'] - Json['PwrT2Give.kWh.min'], 3)
  Json['PwrT2Take.kWh.use'] = round(Json['PwrT2Take.kWh.max'] - Json['PwrT2Take.kWh.min'], 3)
  Json['PwrT2.kWh.use'] = round(Json['PwrT2Take.kWh.use'] - Json['PwrT2Give.kWh.use'], 3)
  Json['Pwr.kWh.use'] = round(Json['PwrT1.kWh.use'] + Json['PwrT2.kWh.use'], 3)
  Index = 'sm-' + Json['CreateTimestamp'][0:4] + '.' + Json['CreateTimestamp'][5:7]
  File = gzip.open(JsonDir + Index + '.gz', 'a')
  print >> File, "{\"index\":{\"_index\":\"%s\",\"_type\":\"doc\",\"_id\":\"%s\"}}" % (Index, Json['CreateTimestamp'])
  print >> File, json.dumps(Json, separators=(',',':'))
  File.close()

#------------------------------------------------------------------------------#
# Main program                                                                 #
#------------------------------------------------------------------------------#
SerialLine = SetupSerialLine()
Avg = {}
Max = {}
Min = {}
Endtime = ''
while True:
  CRCcheck = False
  while CRCcheck == False: 
    Telegram = ReadTelegram(SerialLine)
    try:
      CRC = int(Telegram[-1][1:-2], 16)
      Telegram[-1] = '!'
      CRCcheck = (CRC == CRC16(Telegram))
    except:
      pass
  Dict = Telegram2Dict(Telegram)
  SecStats = InterpretDict(Dict)
  Statistics(SecStats, Min, Max, Avg)
  if Endtime == '':
    Endtime = SecStats['Timestamp'][-8:-5]
    if Endtime >= '500':
      Endtime = '959'
    else:
      Endtime = '459'
  if SecStats['Timestamp'][-8:-5] >= Endtime:
    Stats2Json(Min, Max, Avg)
    Avg = {}
    Max = {}
    Min = {}
    Endtime = ''
