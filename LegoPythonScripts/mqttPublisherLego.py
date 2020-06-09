#!/usr/bin/env pybricks-micropython

# Purpose: transfer EV3 sensor data to Unity through MQTT connection for AR readings
# Finish execution with Ctrl-C
# References:
# https://github.com/JorgePe/ev3-mqtt-micropython


from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.ev3devices import (Motor, TouchSensor, 
          ColorSensor,UltrasonicSensor, GyroSensor)
import sys, os
import ujson, utime


####### MQTT connection ##################
# There are public brokers available but you we can also install
# 'mosquitto' and run our own private broker
# note: ev3dev image already has 'mosquitto' instaled, we can start the
# broker with 'sudo service mosquitto start'

from umqtt.robust import MQTTClient
# broker = "broker.hivemq.com"
# broker="iot.eclipse.org"
MQTT_Broker = 'test.mosquitto.org'

# Define a namespace for all messages
MQTT_Topic_Status = 'EV3ARProject/DataUpload'
# MQTT_Topic_Motor = 'JorgePe/Motor'


########################################################################
# get hostname to use as Client ID
# assuming each EV3 brick had it's hostname changed after installation
########################################################################
os.system('hostname > /dev/shm/hostname.txt')
file = open('/dev/shm/hostname.txt', 'r')
MQTT_ClientID = file.readline().rstrip('\n')
file.close()
os.system('rm /dev/shm/hostname.txt')


#########################################

#Define motor outputs
motor_left = Motor(Port.B)
motor_right = Motor(Port.C)

# Connect EV3 sensors
cl = ColorSensor(Port.S4)
gy = GyroSensor(Port.S2)
ts = TouchSensor(Port.S3)
us = UltrasonicSensor(Port.S1)

###########################################


# returns distance from Ultrasonic Sensor in cm
def getDist():
  dist=us.distance()/10 # convert mm to cm
  # comment back in to filter out 255.0 reading
  # if dist==255.0: 
  #   return 0.0
  return dist  

# returns voltage level of EV3 battery
def getVoltage():
  with open('/sys/devices/platform/battery/power_supply/lego-ev3-battery/voltage_now','r') as f:
    data = f.read()
    # divide by a million for millivolts to volts
    # divide by 9 for fraction of total voltage
    voltage=(float(data)/9000000) 
    return voltage

# callback message to process any new message appearing at the subscribed
# topics
def getmessages(topic, msg):
    if topic == MQTT_Topic_Status.encode():
        brick.display.text(str(msg.decode()))
    elif topic == MQTT_Topic_Motor.encode():
        brick.display.text(str(msg.decode()))
        motor.run_target(180, int(msg.decode()))


########################################################################


# calls thingworxPOST for all sensors while program is running
def uploadData():
  # define and connect to client
  client = MQTTClient(MQTT_ClientID, MQTT_Broker)
  client.connect()
  print("CLIENT CONNECTED")
  while True:
      try:
        dataToUpload = {'distance':getDist(),'color':cl.color(),'angle':(gy.angle() % 360),'touch':ts.pressed(),'power':getVoltage()}
        payload=ujson.dumps(dataToUpload) # convert to a json string
        # client.subscribe("topic/EV3ARProject")
        print(payload)
        client.publish(MQTT_Topic_Status, payload)
        print("payload published")
        utime.sleep(1)
      except KeyboardInterrupt:
        client.disconnect()
        print("\nGoodbye!")
        sys.exit(0)


if __name__=='__main__':
    uploadData()

