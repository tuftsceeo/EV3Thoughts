#!/usr/bin/env pybricks-micropython

# ScriptLego.py
# Purpose: EV3 program code is written and run here!
# This is the microPython version of Script.py
# To run: type "brickrun -r --  pybricks-micropython ScriptLego.py"
# on command line
# NOTE: THIS SCRIPT USES MQTT


from CommandsLego import * # uses functions from EV3ARCommands.py

################## WRITE YOUR CODE BELOW ###############

# Write your code here!
def runInLoop():
 
  while(True):
    forward(5)
    backward(5)
    getTouch()
    getColor()
    getAngle()
    getDist()
    utime.sleep(0.1)
    '''    


    key = input("press a")
    print(key)
    if key == "a":
      print("pressed a")
      left()
    elif key == 'w':
      forward(1)
    elif key == 'd':
      right()
    elif key == 's':
      backward(1)
    
    '''  
 ################### CODE BELOW RUNS PROGRAM; DON'T TOUCH #####################

### This prepares some behind-the-scenes stuff ###

# wrapper for runEV3 that initializes shared values in multiprocessing
# def EV3Program(arr,runCode):
def EV3Program():
  print("in EV3Program")
  # globals.dirArray=arr # sets global array equal to multiprocessing array
  # checkEV3(globals.runCode) # check that all motors and sensors are connected
  runInLoop() # REPLACE WITH CORRECT FUNCTION FROM ABOVE
  globals.running=False # switches boolean to turn off data upload
  print("code is finished! Input anything to quit.")


if __name__=='__main__':
    run(EV3Program)


