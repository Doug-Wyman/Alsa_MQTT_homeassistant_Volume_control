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
from rpi_backlight import Backlight
Version = '2021.10.26.x'
computer = "bedroom"

def get_state():

    global piStateScr, screenlast, piBacklight
    try:
        tmpscr = piBacklight.brightness 
        tmpscr = int(tmpscr)
        piStateScr = tmpscr
        screenlast = tmpscr
    except: 
        print("backlight error")

def get_msg():
    global msg, piBacklight, Version, screenlast, piStateScr
    msg = subscribe.simple('/' + computer + '/Screen/set', hostname=BROKER_ADDRESS)
    #print("%s %s" % (msg.topic, msg.payload))
#    print(str(msg.topic))
#    print(str(msg.payload))
    msg=msg.payload.decode("utf-8","ignore")
#    print("Rxmsg" + msg)
    try:
        tmpdata = msg
#        print("Got scr " + str(tmpdata)) 
        if tmpdata != screenlast:
            if tmpdata == None:
                piBacklight.brightness = int(screenlast)
            else:
                screenlast = tmpdata
                piBacklight.brightness = int(screenlast)
                try:
                    client.connect(BROKER_ADDRESS)
                    client.publish('/' + computer + '/Screen/status', piStateScr)
                    client.publish('/' + computer + '/Screen/xstatus', 'ON')
                    LAST_MESSAGE = time.time()
                except:
                  pass
        piStateScr = int(screenlast) 
 #       print("Success? " + str(piStateScr))
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
 
piBacklight = Backlight()
BROKER_ADDRESS = "192.168.0.109"
BUSY = False
LAST_MESSAGE = time.time()
MESSAGE_INTERVAL = 15
#computer = str(getserial())
client = mqtt.Client(computer + 'scr')
piStateScr = 0
get_state()
time.sleep(4)
#print("----before simple")
get_msg()

try:
    client.connect(BROKER_ADDRESS)
    client.publish('/' + computer + '/Screen/status', piStateScr)
    client.publish('/' + computer + '/Screen/xstatus', 'ON')
    LAST_MESSAGE = time.time()
except:
  pass
 
#print('printed')
screenlast = 20
while True:
    try:
        try:
            get_msg()
        except:
            pass

        if (time.time() - LAST_MESSAGE) > MESSAGE_INTERVAL:
            get_state()
            try:
                client.connect(BROKER_ADDRESS)
                client.publish('/' + computer + '/Screen/status', piStateScr)
                client.publish('/' + computer + '/Screen/xstatus', 'ON')
                LAST_MESSAGE = time.time()
            except:
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
 
