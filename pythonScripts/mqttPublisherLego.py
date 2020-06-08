#!/usr/bin/env pybricks-micropython

# Purpose: transfer EV3 sensor data to Unity through MQTT connection for AR readings
# Finish execution with Ctrl-C
# References:
# https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/
# http://www.steves-internet-guide.com/send-json-data-mqtt-python/
# https://github.com/mqtt/mqtt.github.io/wiki/public_brokers
# http://blog.jorand.io/2017/08/02/MQTT-on-Unity/
# http://www.steves-internet-guide.com/into-mqtt-python-client/

# from ev3dev.ev3 import *
# import ev3dev.ev3 as ev3 # package for EV3 Commands
# import sys
# import linecache
# import requests,json # packages for Thingworx POST & GET
# from time import sleep
# from timeit import Timer

from pybricks.hubs import EV3Brick
from pybricks.tools import wait
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                   SoundFile, ImageFile, Align)
from pybricks.ev3devices import (Motor, TouchSensor, 
          ColorSensor,UltrasonicSensor, GyroSensor)
import sys
import linecache
import os
import ubinascii, ujson, urequests, utime

####### MQTT connection ##################

# import paho.mqtt.client as mqtt
# from umqttsimple import MQTTClient
from umqtt.robust import MQTTClient
# broker = "broker.hivemq.com"
# broker="iot.eclipse.org"
MQTT_Broker = 'test.mosquitto.org'

# def on_message(client, userdata, message):
#     print("message received " ,str(message.payload.decode("utf-8")))
#     print("message topic=",message.topic)
#     print("message qos=",message.qos)
#     print("message retain flag=",message.retain)

#########################################


# global variable for ultrasonic sensor
distance=0


#Define motor outputs
motor_left = Motor(Port.B)
motor_right = Motor(Port.C)

# Connect EV3 sensors
cl = ColorSensor(Port.S4)
gy = GyroSensor(Port.S2)
ts = TouchSensor(Port.S3)
us = UltrasonicSensor(Port.S1)

# define settings for sensors
cl.mode='COL-COLOR' # Color Sensor in COLOR mode
colors=('unknown','black','blue','green','yellow','red','white','brown')
gy.mode='GYRO-ANG' # Put the gyro sensor into ANGLE mode
units = gy.units #reports degrees
us.mode='US-DIST-CM' # Put the US sensor into distance mode
units = us.units # reports 'cm' even though the sensor measures 'mm'

# returns distance from Ultrasonic Sensor in cm
# Note: 255.0 reading is filtered out
def getDist():
  global distance
  dist=us.value()/10 # convert mm to cm
  if dist==255.0:
    return distance
  distance=dist
  return dist  # convert mm to cm

# voltage level of EV3 battery
def getVoltage():
  with open('/sys/devices/platform/battery/power_supply/lego-ev3-battery/voltage_now','r') as f:
    data = f.read()
    # divide by a million for millivolts to volts
    # divide by 9 for fraction of total voltage
    voltage=(float(data)/9000000) 
    return voltage


########################################################################
# get hostname to use as Client ID
# assuming each EV3 brick had it's hostname changed after installation
########################################################################
os.system('hostname > /dev/shm/hostname.txt')
file = open('/dev/shm/hostname.txt', 'r')
MQTT_ClientID = file.readline().rstrip('\n')
file.close()
os.system('rm /dev/shm/hostname.txt')

########################################################################
# There are public brokers available but you we can also install
# 'mosquitto' and run our own private broker
# note: ev3dev image already has 'mosquitto' instaled, we can start the
# broker with 'sudo service mosquitto start'
########################################################################

# Define a namespace for all messages
MQTT_Topic_Status = 'EV3ARProject/DataUpload'
# MQTT_Topic_Motor = 'JorgePe/Motor'


# callback message to process any new message appearing at the subscribed
# topics
def getmessages(topic, msg):
    if topic == MQTT_Topic_Status.encode():
        brick.display.text(str(msg.decode()))
    elif topic == MQTT_Topic_Motor.encode():
        brick.display.text(str(msg.decode()))
        motor.run_target(180, int(msg.decode()))


# This is the Publisher
# broker="iot.eclipse.org"
# client = mqtt.Client()
# #client.on_message = on_message
# client.connect(broker)
# try:
#   #client.on_message=on_message #attach function to callback
#   client.connect(broker)
# except: # TODO: quit after certain amount of time if client can't connect
#   print("CONNECTION FAILED")
#   exit(1)
# client = mqtt.Client()
# client.connect(broker)

client = MQTTClient(MQTT_ClientID, MQTT_Broker)
client.connect()
print("client connected")


####################################################################


# calls thingworxPOST for all sensors while program is running
def uploadData():
  while True:
      try:
        dataToUpload = {'distance':getDist(),'color':colors[cl.value()],'angle':(gy.value() % 360),'touch':ts.value(),'power':getVoltage()}
        payload=json.dumps(dataToUpload) # convert to a json string
        # client.subscribe("topic/EV3ARProject")
        client.publish(MQTT_Topic_Status, payload)
        print("payload published")
        sleep(1)
        #t = Timer(lambda: thingworxPOST(payload)) # for timing PUT request
        #print("Upload time:",t.timeit(number=1))
      except KeyboardInterrupt:
        client.disconnect()
        print("bye!")
        sys.exit(0)


if __name__=='__main__':
    uploadData()

