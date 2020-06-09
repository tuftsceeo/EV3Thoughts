#!/usr/bin/env pybricks-micropython

# Commands.py
# Lily Zhang 
# Purpose: Contains functions to program EV3 movements
# and to upload sensor data
# This is the microPython version of Commands.py
# Uses threading 
# NOTE: THIS SCRIPT USES MQTT

import _thread
import globals # shares global variables with ScriptLego

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)

import ujson, utime
import sys, os

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



# callback message to process any new message appearing at the subscribed
# topics
def getmessages(topic, msg):
    if topic == MQTT_Topic_Status.encode():
        brick.display.text(str(msg.decode()))
    elif topic == MQTT_Topic_Motor.encode():
        brick.display.text(str(msg.decode()))
        motor.run_target(180, int(msg.decode()))


#############################################


# calls thingworxPOST for all sensors while program is running
#def uploadData(arr,runCode):
def uploadData():
  #print("in uploadData")
  #print("value of running:",globals.running)
  client = MQTTClient(MQTT_ClientID, MQTT_Broker)
  client.connect()
  print("CLIENT CONNECTED")
  while globals.running==True:
    try:
      #print("value of running:",globals.running)
      #print("runCode is", runCode)
      #print(arr[:]) 
      # temp = {'forward':arr[0],'right':arr[1],'left':arr[2],'distance':getDist(),'color':colors[cl.value()],'angle':(gy.value() % 360),'touch':ts.value(),'power':getVoltage(),'script':'hello what is happening'}
      temp = {'distance':getDist(),'color':cl.color(),'angle':(gy.angle() % 360),'touch':ts.pressed(),'power':getVoltage()}
      #t = Timer(lambda: thingworxPOST(temp)) # reads time to upload to Thingworx
      #print("Upload time:",t.timeit(number=1))
      payload=ujson.dumps(temp)
      #print(payload)
      client.publish("topic/EV3ARProject", payload)
      print("payload published successfully")
      utime.sleep(.5)
    except:
      print("whoops! Payload not published")
      #runCode=('i',False)
      #break
      #sys.exit()
  #sys.exit()


################# DEFINE MOTOR AND SENSOR VALUES ########################

#Define motor outputs
motor_left = motor_right = None

# Connect EV3 sensors
cl = gy = ts = us = None

# get voltage level of EV3 battery
def getVoltage():
  return brick.battery.voltage()


# Make sure all motors and sensors are properly connected;
# otherwise, stop program execution
# change to appropriate port values here
def checkEV3():
  try:
    global motor_left
    motor_left = Motor(Port.B)
  except:
    print("Oops, left motor is not connected!")
    sys.exit()
  try:
    global motor_right
    motor_right = Motor(Port.C)
  except:
    print("Oops, right motor is not connected!")
    sys.exit()
  try:
    global us
    us = UltrasonicSensor(Port.S1)
  except:
    print("Oops, ultrasonic sensor is not connected!")
    sys.exit()
  try:
    global cl
    cl = ColorSensor(Port.S4)
  except:
    print("Oops, color sensor is not connected!")
    sys.exit()
  try:
    global gy
    gy = GyroSensor(Port.S2)
  except:
    print("oops, gyroscopic sensor is not connected!")
    sys.exit()
  try:
    global ts
    ts = TouchSensor(Port.S3)
  except:
    print("Oops, touch sensor is not connected!")
    sys.exit()
  # print("finished checking EV3")


####################### FUNCTIONS FOR USERS #########################

### GET SENSOR VALUES ###

# returns distance from Ultrasonic Sensor in cm
def getDist():
  dist=us.distance()/10 # convert mm to cm
  # comment back in to filter out 255.0 reading
  # if dist==255.0: 
  #   return 0.0
  return dist  

# returns color detected
def getColor():
  return cl.color()

# returns angle from original at startup
def getAngle():
  return (gy.angle() % 360)

# returns whether touch sensor is pressed
# note: might not work on AR bc touch is so quick
def getTouch():
  return ts.pressed()


### MOTOR CONTROLS ###
# dirArray: [forward, right, left]; 1==true


def forward(time,speed=200,angle=600):
  print("forward")
  # currAngle = angle
  # if angle > 360:
  #   currAngle = getAngle()
  #print("beginning angle is",currAngle)
  # NOTE: cannot be dirArray=[1,0,0] because it is no longer the same array
  # globals.dirArray[0]=1
  # globals.dirArray[1]=0
  # globals.dirArray[2]=0
  motor_left.run(speed)
  motor_right.run(speed)
  utime.sleep(time)
  stop()




# turn EV3 left
# Parameter: degree of turn (0-360)
# Note: turn should be accurate to within 5 degrees
def left():
  print("left")
  # globals.dirArray[0]=0
  # globals.dirArray[1]=0
  # globals.dirArray[2]=1
  # gyroVal=gy.value()
  # print("gyroval is",gyroVal)
  # while gy.value()>=((gyroVal-deg)):
  # #while gy.value()>(gyroVal1-deg+5): 
  #   motor_left.run_direct(duty_cycle_sp=-25)
  #   motor_right.run_direct(duty_cycle_sp=25)
  # stop()
  # print("diff is",abs(gyroVal-gy.value()))
  motor_left.dc(-25)
  motor_right.dc(25)
  utime.sleep(1)
  stop()

# turn EV3 right
# Parameter: degree of turn (0-360)
# Note: turn should be accurate to within 5 degrees
def right():
  # globals.dirArray[0]=0
  # globals.dirArray[1]=1
  # globals.dirArray[2]=0
  # gyroVal=gy.value()
  # print("gyroVal is", gyroVal)
  # while gy.value()<=(gyroVal+deg): 
  #   motor_left.run_direct(duty_cycle_sp=25)
  #   motor_right.run_direct(duty_cycle_sp=-25)
  # stop()
  # print("diff is",abs(gyroVal-gy.value()))
  motor_left.dc(25)
  motor_right.dc(-25)
  utime.sleep(1)
  stop()


def backward(time,speed=200,angle=600):
  # currAngle = angle
  # if angle > 360:
  #   currAngle = getAngle()
  #print("beginning angle is",currAngle)
  print("backward")
  # NOTE: cannot be dirArray=[1,0,0] because it is no longer the same array
  # globals.dirArray[0]=0
  # globals.dirArray[1]=0
  # globals.dirArray[2]=0
  motor_left.run(-speed)
  motor_right.run(-speed)
  utime.sleep(time)
  stop()


# Stop EV3 movement 
def stop():
  motor_left.stop()
  motor_right.stop()



#################### MULTIPROCESSING ############################

# Runs uploadData and EV3Program functions simultaneously
# Parameter: EV3Program function from EV3ARScript
# todo: end everything when one function finishes
def run(func):
  #arr=Array('i',3) # array to hold movement directions
  #runCode= ('i',True) # boolean to end uploadData 
  checkEV3()
  _thread.start_new_thread(uploadData,())
  _thread.start_new_thread(func,())

  # DO NOT DELETE this needs to be here for threading to work 
  input("")

  print("Bye!")