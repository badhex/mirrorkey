# Mirror Key
A python script to monitor the POE log file and press a defined set of keys when detecting a character death.

## Defaults
* The program assumes your capture hotkey is CTRL_r + SHIFT_r + F10.
  * You can simply set your capture hotkey to this combo
  * OR You can modify this in the helpers keysender.py file

## Setup
* Install python and pip
* Clone this repository locally
* Edit the log_file variable in mirrokey.py to point to the correct POE log file. An example location is set by default.
* Install all requirements:
```pip install -r requirements.txt```