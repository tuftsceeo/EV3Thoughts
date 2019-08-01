# TestCommands.py
# Lily Zhang and Mohammed Emun
# 7/30/19
# Purpose: Contains functions to program EV3 movements
# and to upload sensor data to Thingworx;
# Uses multiprocessing to run script from EV3ARScript 
# and upload data simultaneously

from ev3dev.ev3 import *
import ev3dev.ev3 as ev3 # package for EV3 Commands
import sys
import linecache
import requests,json # packages for Thingworx POST & GET
from time import sleep
from multiprocessing import Process,Array,Value
import time,termios,tty
from timeit import Timer
import globals # shares global variables with EV3ARScript

# global variable for ultrasonic sensor
distance=0
colors=('unknown','black','blue','green','yellow','red','white','brown')

################## THINGWORX UPLOAD INFO ##############################

# old Thingworx; may no longer be working?
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
def uploadData(arr,runCode):
  checkEV3(runCode)
  while runCode.value==True:
    try:
      print("runCode is", runCode.value)
      print(arr[:]) 
      temp = {'forward':arr[0],'right':arr[1],'left':arr[2],'distance':getDist(),'color':colors[cl.value()],'angle':(gy.value() % 360),'touch':ts.value(),'power':getVoltage()}
      #thingworxPOST(temp)
      t = Timer(lambda: thingworxPOST(temp)) # reads time to upload to Thingworx
      print("Upload time:",t.timeit(number=1))
    except:
      print("whoops! Something went wrong")
      runCode.value=False




################# DEFINE MOTOR AND SENSOR VALUES ########################

#Define motor outputs
motor_left = ev3.LargeMotor('outB')
motor_right = ev3.LargeMotor('outC')

# Connect EV3 sensors
cl = ColorSensor()
gy = GyroSensor()
ts = TouchSensor()
us = ev3.UltrasonicSensor()


# get voltage level of EV3 battery
def getVoltage():
  with open('/sys/devices/platform/battery/power_supply/lego-ev3-battery/voltage_now','r') as f:
    data = f.read()
    # div by a million for millivolts to volts
    # div by 9 for fraction of total voltage
    voltage=(float(data)/9000000) 
    return voltage

# Make sure all motors and sensors are properly connected;
# otherwise, stop program execution
# Parameter: boolean from multiprocessing to stop uploadData
def checkEV3(runCode):
  try:
    motor_left.run_direct( duty_cycle_sp=0)
  except:
    print("Oops, motor(B) is not connected!")
    runCode.value=False
    exit()
  try:
    motor_right.run_direct( duty_cycle_sp=0)
  except:
    print("Oops, motor(C) is not connected!")
    runCode.value=False
    exit()
  try:
    us.value()
    us.mode='US-DIST-CM' # Put the US sensor into distance mode
    units = us.units # reports 'cm' even though the sensor measures 'mm'
  except:
    print("Oops, ultrasonic sensor is not connected!")
    runCode.value=False
    exit()
  try:
    cl.value()
    cl.mode='COL-COLOR' # Color Sensor in COLOR mode
  except:
    print("Oops, color sensor is not connected!")
    runCode.value=False
    exit()
  try:
    gy.value()
    gy.mode='GYRO-ANG' # Put the gyro sensor into ANGLE mode
    units = gy.units #reports degrees
  except:
    print("oops, gyroscopic sensor is not connected!")
    runCode.value=False
    exit()
  try:
    ts.value()
  except:
    print("Oops, touch sensor is not connected!")
    runCode.value=False
    exit()


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
# note: might not work on AR bc touch is so quick
def getTouch():
  return ts.value()


### MOTOR CONTROLS ###
# dirArray: [forward, right, left]; 1==true

# move EV3 forward 
# Parameters: time to move forward in seconds; optional speed
# Note: if EV3 tilts more than 5 angles off beginning angle,
# self adjust back to acceptable range 
def forward(time,speed=35,angle=600):
  currAngle = angle
  if angle > 360:
    currAngle = getAngle()
  print("beginning angle is",currAngle)
  # NOTE: cannot be dirArray=[1,0,0] because it is no longer the same array
  globals.dirArray[0]=1
  globals.dirArray[1]=0
  globals.dirArray[2]=0
  # autocorrect path every 0.5 seconds
  remTime = time
  while remTime >= .5:
    motor_left.run_direct(duty_cycle_sp=speed)
    motor_right.run_direct(duty_cycle_sp=speed)
    sleep(.5)
    if getAngle() > (currAngle+3)%360 and getAngle() < (currAngle+180)%360:
      print("correcting left")
      left(2)
    elif getAngle() < (currAngle-3)%360 and getAngle() > (currAngle-180)%360:
      print("correcting right")
      right(2)
    print("angle is",getAngle())
    remTime = remTime - .5
  # run for remainder of time
  motor_left.run_direct(duty_cycle_sp=speed)
  motor_right.run_direct(duty_cycle_sp=speed)
  sleep(remTime)
  stop()




# turn EV3 left
# Parameter: degree of turn (0-360)
# Note: turn should be accurate to within 5 degrees
def left(deg):
  globals.dirArray[0]=0
  globals.dirArray[1]=0
  globals.dirArray[2]=1
  gyroVal=gy.value()
  print("gyroval is",gyroVal)
  while gy.value()>=((gyroVal-deg)):
  #while gy.value()>(gyroVal1-deg+5): 
    motor_left.run_direct(duty_cycle_sp=-25)
    motor_right.run_direct(duty_cycle_sp=25)
  stop()
  print("diff is",abs(gyroVal-gy.value()))

# turn EV3 right
# Parameter: degree of turn (0-360)
# Note: turn should be accurate to within 5 degrees
def right(deg):
  globals.dirArray[0]=0
  globals.dirArray[1]=1
  globals.dirArray[2]=0
  gyroVal=gy.value()
  print("gyroVal is", gyroVal)
  while gy.value()<=(gyroVal+deg): 
    motor_left.run_direct(duty_cycle_sp=25)
    motor_right.run_direct(duty_cycle_sp=-25)
  stop()
  print("diff is",abs(gyroVal-gy.value()))


# move EV3 backward
# Parameters: time to move backward in seconds; optional speed
# Note: if EV3 tilts more than 5 angles off beginning angle,
# self adjust back to acceptable range 
def backward(time,speed=35,angle=600):
  currAngle = angle
  if angle > 360:
    currAngle = getAngle()
  print("beginning angle is",currAngle)
  globals.dirArray[0]=0
  globals.dirArray[1]=0
  globals.dirArray[2]=0
  # autocorrect path every 0.5 seconds
  remTime = time
  while remTime >= .5:
    motor_left.run_direct(duty_cycle_sp=-speed)
    motor_right.run_direct(duty_cycle_sp=-speed)
    sleep(.5)
    if getAngle() > (currAngle+3)%360 and getAngle() < (currAngle+180)%360:
      print("correcting left")
      left(2)
    if getAngle() < (currAngle-3)%360 and getAngle() > (currAngle-180)%360:
      print("correcting right")
      right(2)
    print("angle is",getAngle())
    remTime = remTime - .5
  # run for remainder of time
  motor_left.run_direct(duty_cycle_sp=-speed)
  motor_right.run_direct(duty_cycle_sp=-speed)
  sleep(remTime)
  stop()


# Stop EV3 movement 
def stop():
  motor_left.run_direct( duty_cycle_sp=0)
  motor_right.run_direct( duty_cycle_sp=-0)



#################### MULTIPROCESSING ############################

# Runs uploadData and EV3Program functions simultaneously
# Parameter: EV3Program function from EV3ARScript
# todo: end everything when one function finishes
def run(func):
  arr=Array('i',3) # array to hold movement directions
  runCode= Value('i',True) # boolean to end uploadData 
  p1 = Process(target = uploadData,args=(arr,runCode))
  p2 = Process(target = func,args=(arr,runCode))
  p1.start()
  p2.start()
  p1.join()
  p2.join()