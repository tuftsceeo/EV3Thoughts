# uploadData.py
# Lily Zhang
# 7/30/19
# Purpose: upload EV3 data to Thingworx through REST APIs for AR readings
# Note: each PUT request takes approximately 2-4 seconds
# Finish execution with Ctrl-C

from ev3dev.ev3 import *
import ev3dev.ev3 as ev3 # package for EV3 Commands
import sys
import linecache
import requests,json # packages for Thingworx POST & GET
from time import sleep
from timeit import Timer

# global variable for ultrasonic sensor
distance=0

# Thingworx info
# old Thingworx
# uploading to this one takes about 0.6 seconds
# url = "http://pp-1804271345f2.portal.ptc.io:8080/Thingworx/Things/Lily_Emun_2019/Properties/"
# headers = {
#        'appKey': "f76e9513-0bbc-4b33-af7f-09e5ea959504",
#        'Accept': "application/json",
#        'Content-Type': "application/json"
#        }

# # new Thingworx
url = "https://ptcacademic-dev3-twx.es.thingworx.com/Thingworx/Things/AR_Project/Properties/"
headers = {
        'appKey': "9e2960df-5b7c-476c-8b60-3d9b77037a28",
        'Accept': "application/json",
        'Content-Type': "application/json"
        }

#Define motor outputs
motor_left = ev3.LargeMotor('outB')
motor_right = ev3.LargeMotor('outC')

# Connect EV3 sensors
cl = ColorSensor()
gy = GyroSensor()
ts = TouchSensor()
us = ev3.UltrasonicSensor()

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


# Post property value to thingworx
# propvalue format: {'variableName':variableValue}
def thingworxPOST(propValue):
   requests.request("PUT",url+'*',headers=headers,json=propValue)


# calls thingworxPOST for all sensors while program is running
def uploadData():
   while True:
      try:
        payload = {'distance':getDist(),'color':colors[cl.value()],'angle':(gy.value() % 360),'touch':ts.value(),'power':getVoltage()}
        t = Timer(lambda: thingworxPOST(payload)) # for timing PUT request
        # thingworxPOST(payload)
        print("Upload time:",t.timeit(number=1))
      except KeyboardInterrupt:
        print("bye!")
        sys.exit(0)


if __name__=='__main__':
    uploadData()

