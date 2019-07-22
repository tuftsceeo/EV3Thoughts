# TestScript.py
# 7/22/19
# EV3 program code is written and run here!

from TestCommands import *
import globals


###################### INFO ##########################

# Goal: work with your team to move your EV3 robot through an obstacle course!
# Using the augmented reality app, you can "see" what the robot is sensing.
# Note: EV3 sensors are not the most advanced or accurate. It is helpful to use AR
# to see the limitations of the sensors and the capabilities of the EV3.
# In addition, there will be a bit of delay in the AR visualizations in the app,
# due to a time lag while uploading data.
# The data will update fully if EV3 is paused for several seconds.

# To stop execution of program, Ctrl-C.

# FUNCTIONS AVAILABLE:
# getDist(): returns distance from nearest obstacle in cm
# getColor(): colors available = 'unknown','black','blue','green','yellow','red','white','brown'
# getAngle(): returns angle offset from starting position (0 to 360 degrees)
# getTouch(): returns 1 if touch sensor is pushed, 0 if not; takes ~2 seconds to update;
# sensor must be held down for result
# forward(numSeconds,speed): moves robot forward for numSeconds; speed is optional argument;
# default speed is 35
# back(numSeconds,speed): moves robot backward for numSeconds; speed is optional argument; 
# default speed is 35
# left(numDegrees): turns robot left numDegrees (0-360); accurate to approx 5 degrees
# right(numDegrees): turns robot right numDegrees (0-360); accurate to approx 5 degrees
# stop(): stops robot movement
# sleep(float): pauses for given amount of time
# print("body of print"): prints debug statements to terminal
# printAR("hello world"): prints debug statements to text panel in AR app

# NOTE: The EV3 will stop moving after each function is finished running.

# Feel free to use conditional statements (while, if, etc) and other methods 
# to move your robot through the obstacle course!

# Example code: 
#    while (getColor() != 'green'):
#        forward(1)
#    stop()
#    left(90)
#    forward(2,40)
#    stop()
#    forward(1)


######################### WRITE YOUR CODE BELOW #################################



# Write your code here!
def runEV3():
  while True:
    forward(2)
    left(90)
    right(90)
    back(2)






 ##################### CODE BELOW RUNS PROGRAM; DON'T TOUCH #######################

# This prepares some behind-the-scenes stuff
def EV3Program(arr):
    globals.dirArray=arr
    sleep(2)
    runEV3()


# This runs the function, runEV3, that contains your program  
if __name__=='__main__':
    run(EV3Program)