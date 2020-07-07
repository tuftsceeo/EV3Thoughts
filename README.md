# Augmented Reality App for Visualizing EV3 Sensor Data
Tufts University Center for Engineering Education and Outreach  
Summer 2019-2020  
Main Contributors: Lily Zhang, Mohammed Emun  

**UPDATES: should currently edit and push to LegoEd branch!**

Notes on running Micropython from terminal:  
 *To start REPL: brickrun -r --  pybricks-micropython    
 *To exit REPL: Ctrl-d  
 *To run program: brickrun -r --  pybricks-micropython “programName.py”  
 *Can also run regular python by starting python interpreter


This Unity project visualizes EV3 sensor data published from an EV3 run with EV3DEV.

The project is currently using **MQTT** to publish data to a public broker. Can be adjusted to use **REST APIs** to publish data to Thingworx Composer instead - see files below (**will need a Composer account**).

*ARSensorInterface*: Unity project containing AR app. textEdit.cs, found under Assets, contains the sensor data retrieval code and more information about how to modify it for REST APIs or MQTT.

*pythonScripts*: folder containing python scripts to run with EV3DEV
  * *Commands.py*: contains functions for movement, sensor data retrieval, and sensor data upload  
  * *Script.py*: editable file to run EV3 while uploading data (**Call this file in terminal**) 
  * *EV3ARInfo.txt*: documentation for functions in Commands.py
  * *EV3ARCommands.py*: contains functions for movement, sensor data retrieval, and sensor data upload, using REST APIs (**Account may no longer be active**)
  * *EV3ARScript.py*: editable file to run EV3 while uploading data using REST APIs (**Account may no longer be active**)
  * *apiPublisher.py*: continuously uploads sensor data to Thingworx Composer using REST APIs (**Account may no longer be active**)
  * *mqttPublisher.py*: continuously uploads sensor data to MQTT broker 
  * *driveEV3.py*: allows user to move EV3 around with keyboard
  * *globals.py*: contains shared variables between Commands.py and Script.py; do not edit 
  * *sftp-config.json*: sets up remote connection from terminal to EV3

*LegoPythonScripts*: folder containing pythong scripts to run with Lego Education Micropython (files that start with *Lego* have the same purposes as those listed above)

*thingmark.docx*: image target for AR app.

An example project can be found at https://www.steamdiscoverylab.com/ar-obstacle-course-with-ev3.html  

More documentation on Unity, Thingworx, and working with the EV3 (**including setup and code execution**) can be found at https://docs.google.com/document/d/1_b_NURj-R-_8KY1QK9YQbj9vGlIBPN0UUgQzuAot95U/edit?usp=sharing

Changes made to connect EV3Thoughts with Unity project:
- changed broker name to "broker.hivemq.com" in CommandsLego.py
- changed the topic name to "topic/EV3ARProject"
- changed the return type of getColor() function in CommandsLego.py to string.
- changed the return type of getTouch() function in CommandsLego.py to int.
- changed the recieving script textEditor.cs to match the changes made in CommandsLego.py
- changed the vuforia target image to a 3D scan of the EV3 brick.

To run EV3Thoughts:
- In a terminal window, ssh into the EV3 with: `$ ssh robot@IPAddress` and enter password.
- Navigate to the LegoPythonScripts directory.
- Run the ScriptLego.py script with: `$ brickrun -r -- pybricks-micropython ScriptLego.py`
- Open Unity project, connect USB camera and select said camera within the "AR Camera" Game Object located within the Hierachy > Open Vuforia Engine Configuration > Camera Device. 
- Hit the play button, then hit start (no host, U/N is necessary) and focus the USB camera on the EV3 robot (You should see a Sensor Panel with the current sensor readings). 


