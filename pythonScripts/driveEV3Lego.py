#!/usr/bin/env pybricks-micropython

# Lily Zhang
# adapted from Dan McGinn
# Purpose: drive EV3 with keyboard inputs
# This is the microPython version of driveEV3.py
# Run with "brickrun -r --  pybricks-micropython driveEV3Lego.py"


from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.ev3devices import (Motor, TouchSensor, 
          ColorSensor,UltrasonicSensor, GyroSensor)
import sys, os
import utime

#########################################

#Define motor outputs
motor_left = Motor(Port.B)
motor_right = Motor(Port.C)
speed = 300 # Set Speed

# Connect EV3 sensors
cl = ColorSensor(Port.S4)
gy = GyroSensor(Port.S2)
ts = TouchSensor(Port.S3)
us = UltrasonicSensor(Port.S1)

###########################################

# Initiate keybaord inputs
def getch():
    import termios, tty, sys
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    except: 
      ch = None
    # finally:
    #     termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def forward():
   motor_left.run(speed)
   motor_right.run(speed)
   utime.sleep(.6)
   stop()
def back():
   motor_left.run(-speed)
   motor_right.run(-speed)
   utime.sleep(.6)
   stop()
def left():
   motor_left.run(-speed)
   motor_right.run(speed)
   utime.sleep(.40)
   stop()
def right():
   motor_left.run(speed)
   motor_right.run(-speed)
   utime.sleep(.40)
   stop()
def stop():
   motor_left.stop()
   motor_right.stop()
# def red():
#     ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
#     sleep(0.01)
#     ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
#     sleep(0.01)
# def orange():
#     ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)
#     sleep(0.01)
#     ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
#     sleep(0.01)
# def yellow():
#     ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
#     sleep(0.01)
#     ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
#     sleep(0.01)
# def green():
#     ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
#     sleep(0.01)
#     ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
#     sleep(0.01)

print("-----------Connection Initiated-----------")
while True:
   char = getch()
   if char == 'w':
      forward()
      print("Forward")
   if char == 's':
      back()
      print("Backward")
   if char == 'a':
      left()
      print("Left")
   if char == 'd':
      right()
      print("Right")
   if char == ' ':
      stop()
   #    ev3.Leds.all_off()
   # if char == 'r':
   #    red()
   #    print("Red")
   # if char == 'o':
   #    orange()
   #    print("Orange")
   # if char == 'y':
   #    yellow()
   #    print("Yellow")
   # if char == 'g':
   #    green()
   #    print("Green")
   if char == 'q':
      print("-------------------EXIT-------------------")
      utime.sleep(0.01)
      stop()
      # ev3.Leds.all_off()
      sys.exit()
