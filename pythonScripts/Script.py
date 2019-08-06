# TestScript.py
# 8/5/19
# Purpose: EV3 program code is written and run here!
# To run: type "python3 EV3ARScript.py" on command line
# NOTE: PROGRAM LOADS FOR ABOUT 30 SECONDS BEFORE RUNNING
# NOTE: THIS SCRIPT USES MQTT

from Commands import * # uses functions from EV3ARCommands.py
import globals # uses global variable


################## WRITE YOUR CODE BELOW ###############

# Write your code here!
def runEV3():
  while True:
    while getColor() != 'red':
      forward(.5,25)
      sleep(4)
    left(90)
    sleep(4)
    while getDist() > 7:
      forward(.5,25)
      sleep(4)
    right(180)
    forward(2,25)
    sleep(4)
    right(90)
    sleep(4)
    forward(3,25)
    sleep(4)
    right(180)
    sleep(4)

def runInLoop():
  while True:
    print("hello")
    sleep(5)


 ################### CODE BELOW RUNS PROGRAM; DON'T TOUCH #####################

### This prepares some behind-the-scenes stuff ###

# wrapper for runEV3 that initializes shared values in multiprocessing
def EV3Program(arr,runCode):
    globals.dirArray=arr # sets global array equal to multiprocessing array
    checkEV3(runCode) # check that all motors and sensors are connected
    runInLoop() # runs EV3 code
    runCode.value=False # switches boolean to turn off data upload


if __name__=='__main__':
    run(EV3Program)


