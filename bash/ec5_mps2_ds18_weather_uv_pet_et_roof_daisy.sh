#!/bin/bash
# this scripts wirte the detail about what is going to be sent through email
# for example the new ip address, whether the sensors/programs is working and so on.

sleep 18 
#su pi
cd /home/pi/pyduino/python/
#python rs232_adam.py
python ec5_mps2_ds18_weather_uv_pet_et_roof_daisy.py
