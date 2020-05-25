# Augmented Reality App for Visualizing EV3 Sensor Data
Tufts University Center for Engineering Education and Outreach  
Summer 2019  
Main Contributors: Lily Zhang, Mohammed Emun  

This Unity project visualizes EV3 sensor data published from an EV3 run with EV3DEV.

The project is currently using **MQTT** to publish data to a public broker. Can be adjusted to use **REST APIs** to publish data to Thingworx Composer instead - see files below (**will need a Composer account**).

*ARSensorInterface*: Unity project containing AR app. textEdit.cs, found under Assets, contains the sensor data retrieval code and more information about how to modify it for REST APIs or MQTT.

*pythonScripts*: folder containing python scripts to run on EV3 (using EV3DEV)
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

*thingmark.docx*: image target for AR app.

An example project can be found at https://www.steamdiscoverylab.com/ar-obstacle-course-with-ev3.html  

More documentation on Unity, Thingworx, and working with the EV3 (**including setup and code execution**) can be found at https://docs.google.com/document/d/1_b_NURj-R-_8KY1QK9YQbj9vGlIBPN0UUgQzuAot95U/edit?usp=sharing
