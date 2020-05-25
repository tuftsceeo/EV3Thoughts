# Augmented Reality App for Visualizing EV3 Sensor Data
Tufts University Center for Engineering Education and Outreach  
Summer 2019  
Main Contributors: Lily Zhang, Mohammed Emun  

This Unity project visualizes EV3 sensor data published from an EV3 run with EV3DEV.

All files are currently using MQTT to publish data to a public broker, unless otherwise specified.

ARSensorInterface: Unity project containing AR app. textEdit.cs, found under Assets, contains the sensor data retrieval code and more information about how to modify it.

pythonScripts: folder containing python scripts to run on EV3 (using EV3DEV)  
Commands.py: contains functions for sensors/movement, uploads sensor data  
Script.py: editable file to run EV3 while uploading data  
uploadData.py: continuously uploads sensor data  
CommandsAPI.py: uses REST APIs, uploads to Thingworx Composer  
globals.py: contains shared variables between Commands and Script  
uploadDataAPI.py: uses REST APIs, uploads to Thingworx Composer  

thingmark.docx: image target for AR app.

An example project can be found at https://www.steamdiscoverylab.com/ar-obstacle-course-with-ev3.html  
More documentation on Unity, Thingworx, and working with the EV3 can be found at https://docs.google.com/document/d/1_b_NURj-R-_8KY1QK9YQbj9vGlIBPN0UUgQzuAot95U/edit?usp=sharing
