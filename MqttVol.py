""" Docstring
    This module interfaces a raspberry pi's various functions 
    to Home Assistant through the MQTT interface
"""
import os
import sys
import time
import asyncio
import json
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import alsaaudio
Version = '2021.10.26.x'
computer = "bedroom"

def get_state():

    global piStateVol, piVolume, volumelast
    try:
        piVolume = alsaaudio.Mixer(alsaaudio.mixers()[0])
        tmpvol = (piVolume.getvolume()[0])
        piStateVol = tmpvol
        volumelast = tmpvol
    except: 
        print("volume error")

def get_msg():
    global msg, piVolume, Version, volumelast, piStateVol
    msg = subscribe.simple('/' + computer + '/volume/set', hostname=BROKER_ADDRESS)
    #print("%s %s" % (msg.topic, msg.payload))
#    print(str(msg.topic))
#    print(str(msg.payload))
    msg=msg.payload.decode("utf-8","ignore")
#    print("Rxmsg" + msg)
    try:
        tmpdata = msg
        #print("Got vol " + str(tmpdata)) 
        if int(tmpdata) != int(volumelast):
            if tmpdata == None:
                piVolume.setvolume(int(volumelast))
            else:
                volumelast = int(tmpdata)
                piVolume.setvolume(int(volumelast))
                try:
                    client.connect(BROKER_ADDRESS)
                    client.publish('/' + computer + '/volume/status', volumelast)
                    client.publish('/' + computer + '/volume/xstatus', 'ON')
                    LAST_MESSAGE = time.time()
                except:
                  pass
        piStateVol = int(volumelast) 
        #print("Success?")
        time.sleep(.25)
    except:
        pass

try:
    myconf = open('/var/www/html/RpiMqtt.conf', 'r')
    myline = myconf.readline()
    while myline:
        if myline[:8] == 'computer':
            computer = myline[8:].strip()
            print("Got computer:" + computer )
        myline = myconf.readline()
    myconf.close()
except:
    pass

piStatevol = ""
print(alsaaudio.mixers()[0])
piVolume = alsaaudio.Mixer(alsaaudio.mixers()[0])
BROKER_ADDRESS = "192.168.0.109"
BUSY = False
LAST_MESSAGE = time.time()
MESSAGE_INTERVAL = 15
client = mqtt.Client(computer + 'vol')
get_state()
time.sleep(4)
get_msg()
try:
    client.connect(BROKER_ADDRESS)
    client.publish('/' + computer + '/volume/status', volumelast)
    client.publish('/' + computer + '/volume/xstatus', 'ON')
    LAST_MESSAGE = time.time()
except Exception as e: 
  print(e)
  pass

print('printed')
while True:
    try:
        try:
            get_msg()
        except Exception as e: 
            print(e)
            pass

        if (time.time() - LAST_MESSAGE) > MESSAGE_INTERVAL:
            get_state()
            try:
                client.connect(BROKER_ADDRESS)
                client.publish('/' + computer + '/volume/status', volumelast )
                client.publish('/' + computer + '/volume/xstatus', 'ON')
                LAST_MESSAGE = time.time()
            except Exception as e: 
              print(e)
              #print("connect error")
              pass

        time.sleep(1)
    except OSError as e:
        print("OOPs")
        print(str(e))
        print("os error")
        pass

    except KeyboardInterrupt as e:
        print("OOPs")
        print(str(e))
        print("os error")
        sys.exit("Error message")
    except AttributeError as e:
        print("OOPs")
        print(str(e))
        print("attribute error")
        sys.exit("Error message")

