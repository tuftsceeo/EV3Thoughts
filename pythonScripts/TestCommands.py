# TestCommands.py
# Lily Zhang and Mohammed Emun
# 7/22/19
# Reads EV3 sensor data and uploads to Thingworx;
# Contains functions students can use to program EV3;
# "Run" function uploads data and runs TestScript with multiprocessing

from ev3dev.ev3 import *
import ev3dev.ev3 as ev3 # package for EV3 Commands
import sys
import linecache
import requests,json # packages for Thingworx POST & GET
from time import sleep
from multiprocessing import Process,Array,Value
from timeit import Timer
import globals

# global variable for ultrasonic sensor
distance=0

################## THINGWORX UPLOAD INFO ##############################

# old Thingworx
# uploading to this one takes about 0.6 seconds
# url = "http://pp-1804271345f2.portal.ptc.io:8080/Thingworx/Things/Lily_Emun_2019/Properties/"
# headers = {
#        'appKey': "f76e9513-0bbc-4b33-af7f-09e5ea959504",
#        'Accept': "application/json",
#        'Content-Type': "application/json"
#        }

# new Thingworx
url = "https://ptcacademic-dev3-twx.es.thingworx.com/Thingworx/Things/AR_Project/Properties/"
headers = {
        'appKey': "9e2960df-5b7c-476c-8b60-3d9b77037a28",
        'Accept': "application/json",
        'Content-Type': "application/json"
        }


# Post property value to thingworx
# propvalue format: {'variableName':variableValue}
def thingworxPOST(propValue):
   requests.request("PUT",url+'*',headers=headers,json=propValue)


# calls thingworxPOST for all sensors while program is running
def uploadData(arr):
   while True:
      try:
        print(arr[:]) 
        temp = {'forward':arr[0],'right':arr[1],'left':arr[2],'distance':getDist(),'color':colors[cl.value()],'angle':(gy.value() % 360),'touch':ts.value(),'power':getVoltage()}
        #thingworxPOST(temp)
        t = Timer(lambda: thingworxPOST(temp)) # reads time to upload to Thingworx
        print("Time to upload: ",t.timeit(number=1))
      except KeyboardInterrupt:
        print("bye")
        sys.exit(0)



################# DEFINE MOTOR AND SENSOR VALUES ########################

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

# voltage level of EV3 battery
# TODO: should send float to Thingworx and print battery level as float in Unity
def getVoltage():
  with open('/sys/devices/platform/battery/power_supply/lego-ev3-battery/voltage_now','r') as f:
    data = f.read()
    # div by a million for millivolts to volts
    # div by 9 for fraction of total voltage
    voltage=(float(data)/9000000) 
    # print('{:.1%}'.format(voltage))
    return voltage


####################### FUNCTIONS FOR USERS #########################

# Print out debug statement to AR panel
def printAR(string):
 thingworxPOST({'script':string})

### GET SENSOR VALUES ###

# returns distance from Ultrasonic Sensor in cm
# Note: 255.0 reading is filtered out
def getDist():
   global distance
   dist=us.value()/10 # convert mm to cm
   if dist==255.0:
       return distance
   distance=dist
   return dist  # convert mm to cm

# returns color detected
def getColor():
   return colors[cl.value()]

# returns angle from original at startup
def getAngle():
   return (gy.value() % 360)

# returns whether touch sensor is pressed
# note: might not work bc touch is so quick
def getTouch():
 return ts.value()

### MOTOR CONTROLS ###

# go forward for given time; speed is optional
def forward(time,speed=35):
  temp = {'forward': 1,'right': 0,'left': 0}
  #thingworxPOST(temp)
  #global dirArray
  #print("in forward, dirArray is ", dirArray[:])
  # NOTE: cannot be dirArray=[1,0,0] because it is no longer the same array
  globals.dirArray[0]=1
  globals.dirArray[1]=0
  globals.dirArray[2]=0
  motor_left.run_direct(duty_cycle_sp=speed)
  motor_right.run_direct(duty_cycle_sp=speed)
  sleep(time)
  stop_robot()

# turn left given degrees
def left(deg):
  temp = {'forward': 0,'right': 0,'left': 1}
  #thingworxPOST(temp)
  #global dirArray
  globals.dirArray[0]=0
  globals.dirArray[1]=0
  globals.dirArray[2]=1
  gyroVal1=gy.value()
  while gy.value()>(gyroVal1-deg+5): 
    motor_left.run_direct(duty_cycle_sp=-30)
    motor_right.run_direct(duty_cycle_sp=30)
  stop_robot()

# turn right given degrees
def right(deg):
  temp = {'forward': 0,'right': 1,'left': 0}
  #thingworxPOST(temp)
  #global dirArray
  globals.dirArray[0]=0
  globals.dirArray[1]=1
  globals.dirArray[2]=0
  gyroVal2=gy.value()
  while gy.value()<(gyroVal2+deg-5): 
    motor_left.run_direct(duty_cycle_sp=30)
    motor_right.run_direct(duty_cycle_sp=-30)
  stop_robot()

# move backwards
def back(time,speed=35):
  temp = {'forward': 0,'right': 0,'left': 0}
  #thingworxPOST(temp)
  #global dirArray
  #dirArray[0]=0
  #dirArray[1]=0
  #dirArray[2]=0
  motor_left.run_direct(duty_cycle_sp=-speed)
  motor_right.run_direct(duty_cycle_sp=-speed)
  sleep(time)
  stop_robot()

# called by user to stop robot
def stop():
  motor_left.run_direct( duty_cycle_sp=0)
  motor_right.run_direct( duty_cycle_sp=-0)
  #temp = {'forward': 0,'right': 0,'left': 0}
  #thingworxPOST(temp)

# called in every motor function
def stop_robot():
  motor_left.run_direct( duty_cycle_sp=0)
  motor_right.run_direct( duty_cycle_sp=-0)



#################### MULTIPROCESSING ############################

# for multiprocessing: runs both functions called
# parameter: testMe function from TestScript
# todo: end everything when one function finishes
def run(func):
   arr=Array('i',3)
   p1 = Process(target = uploadData,args=(arr,))
   p2 = Process(target = func,args=(arr,))
   p1.start()
   p2.start()
   p1.join()
   p2.join()