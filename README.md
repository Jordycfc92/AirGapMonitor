# Lidar-Lite

## Libraries for interacting with Lidar-Lite over I2C

This library will only work in a linux environment
please install i2c-dev and i2c-tools

For recent Raspberry Pis or if you get an error such as 

`/src/lidar_lite.cpp:36:64: error: ‘i2c_smbus_write_byte_data’ was not declared in this scope`

use this command to install `i2c-dev`:

`apt-get install libi2c-dev`

If you wish to test this software you will need to use either and Linux distro or MacOS system, it will not open on windows due to the missing 'fcntl' module.

To use this application, first install the packages listed in the requirements.txt file using 'pip install -r requirements.txt'.

You'll need an API key from Stormglass.io in the config.env file. You will also need to change the path to that file in the constructor of the OperationMonitor file. 

Start the application from the GUI.py file
