Hello,
initial commit

NO DOCKER

1. setup pi
2. connect via SSH
3. run 

````
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git mosquitto mosquitto-clients -y
pip3 install flask paho-mqtt RPi.GPIO
````


install venv
sudo apt install python3-venv -y
create 
python3 -m venv ~/fermentation-venv
activate

source ~/fermentation-venv/bin/activate

within venv installl py packages 

pip install --break-system-packages flask paho-mqtt RPi.GPIO

verify installation:

python3 -c "import flask, paho.mqtt.client, RPi.GPIO; print('Success!')"

make venv persistent
echo "source ~/fermentation-venv/bin/activate" >> ~/.bashrc
source ~/.bashrc

pip install --upgrade pip
pip install --break-system-packages flask paho-mqtt RPi.GPIO

confirm installation
pip list | grep -E 'flask|paho-mqtt|RPi.GPIO'

## initialize TEMP SENSOR
check if enabled
ls /sys/bus/w1/devices/


if not manually
sudo nano /boot/firmware/config.txt

add this to the bottom
dtoverlay=w1-gpio

then reboot
sudo reboot

If you see directories like 28-XXXXXXXXXXXX, your DS18B20 sensors are detected.

## Initialize mqtt
ensure broker running

subscribe from Tool
publish from other device 
e.g. on mac 
mosquitto_pub -h 192.168.0.209 -t "/control/fermentation_chamber/controller/2B3C4D" -m "Test Command from Mac"

## Test Relays




## Before Usage
-> run all test scripts manually 1 by 1 

## Enable I2C

sudo raspi-config
Interfacing Options → I2C → Enable.

Display Pin	Raspberry Pi Pin	Function
GND	Pin 6	Ground
VDD	Pin 1 (3.3V) or Pin 2 (5V)	Power
SCK (Clock)	Pin 5 (GPIO 3, SCL)	I2C Clock
SDA (Data)	Pin 3 (GPIO 2, SDA)	I2C Data

sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- 3C -- -- -- -- -- -- --

sudo apt install -y i2c-tools
pip install smbus2 pillow

pip install luma.oled luma.core

## Setup USB Power control

sudo apt update
sudo apt install uhubctl

List available hubs & ports
sudo uhubctl

expected output similar to
Current status for hub 1-1 [0424:9514, USB 2.00, 5 ports, ppps]
  Port 1: 0503 power highspeed enable connect [0424:ec00]
  Port 2: 0100 power
  Port 3: 0100 power
  Port 4: 0100 power
  Port 5: 0100 power

  turn off all
  sudo uhubctl -a off -l 1-1
turn on all

turn off PORT_NO
sudo uhubctl -a off -l 1-1 -p PORT_NO
sudo uhubctl -a off -l 1-1 -p 2
´
turn on PORT_NO
sudo uhubctl -a on -l 1-1 -p PORT_NO
sudo uhubctl -a on -l 1-1 -p 2


## TESTABLE FILES
relay_control.py
fan_control.py

### Part list
### downloadable stl files for 3d printing house


# PRIOR to assembly -> Auto - Start
when all up and running ensure, system auto starts on boot 

add start_button.py to systemd for autostart when starting in bg automatically and restart after crash
sudo nano /etc/systemd/system/start_button.service

add
````
[Unit]
Description=Start Button for Fermentation Chamber
After=multi-user.target

[Service]
ExecStart=/home/brewmaster/fermentation-venv/bin/python3 /home/brewmaster/Desktop/hasabrewery-fermentation-chamber/start_button.py
WorkingDirectory=/home/brewmaster/Desktop/hasabrewery-fermentation-chamber
StandardOutput=inherit
StandardError=inherit
Restart=always
User=brewmaster

[Install]
WantedBy=multi-user.target
````

run
sudo systemctl daemon-reload
sudo systemctl enable start_button.service
sudo systemctl start start_button.service

check if services are running
sudo systemctl status start_button.service

expected output
● start_button.service - Start Button for Fermentation Chamber
   Loaded: loaded (/etc/systemd/system/start_button.service; enabled)
   Active: active (running) since ...

##

# send command to Chamber
mosquitto_pub -h 192.168.0.209 -t "/control/fermentation_chamber/controller/2B3C4D" -m '{
    "message": "Test",
    "fermentation": {
        "stages_numbers": 3,
        "schedule": [
            {
                "stage": "Other Stage",
                "temperature": {
                    "value": 40,
                    "unit": "Celsius"
                },
                "pressure": {
                    "value": 24,
                    "unit": "psi"
                },
                "time": {
                    "value": 5,
                    "unit": "days"
                },
                "additive": {
                    "name": "Yeast Nutrient",
                    "value": 2,
                    "unit": "g"
                },
                "comments": "Start primary fermentation"
            }
        ]
       
    },
    "recipe_data": {
        "id": "ABC123",
        "name": "Test Brew3"
    }
}'