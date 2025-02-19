# 🍺 HasABrewery Fermentation Chamber | Full Control - Plug & Play
[![Version](https://img.shields.io/badge/version-1.0.1-brightgreen)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)  
[![Platform](https://img.shields.io/badge/platform-ESP32-orange)](https://espressif.com/)

## 🚀 ChEAPER THAN INKBIRD & Fully Connected
The Fermentation Chamber Controller is a Raspberry Pi-based system for automating temperature control in fermentation. 
It integrates **DS18B20 sensors**, **MQTT communication**, **relay control**, and an **OLED display**. This project 
ensures optimal fermentation conditions, supports remote monitoring, and is part of the **Has A Brewery Ecosystem**.

### NOTES - to be added
- party list / AWS links

## 📌 Features
- 🛠️ **Plug & Play setup** - simply go thru docs here and follow along!.
- ✅ **Fully Automated Fermentation Control** with real-time monitoring.
- 🔘 **Start-Stop Button** with proper boot-up / power-down logic
- 🎮 **Smart & PID Controlls** for intelligent temperature regulations.
- 🖥️ **OLED Display Support** for live status updates.
- 📡 **MQTT-Based Communication** for seamless integration.
- 🌡️ **DS18B20 Temperature Sensors** for precise readings.
- 🔌 **Relay-Controlled Heating and Cooling** based in intelligent sensors.

## Overview
This project provides an automated and remote-controlled fermentation chamber to ensure optimal brewing conditions. It is fully modular, allowing you to start with a simple setup and expand over time. Whether you use all available sensors—such as temperature probes, fans, relays, door sensors, and displays—or just a few, the system remains fully operational. Active support ensures you can integrate new components as needed while keeping everything running smoothly. The chamber can be as simple or advanced as you want, making it ideal for both beginners and expert brewers. Start now with the basics and scale up over time while utilizing only the hardware you already have!

## Platform
- **Target Device**: Raspberry Pi
- **Operating System**: Raspberry Pi 3 (and later) OS 64-bit (recommended)

## Installation & Preparation
### Prerequisites
Ensure you have:
- a **Raspberry Pi** (any model with GPIO support)
- an **SD card** with Raspberry Pi OS installed
- an **Internet connection** and local network (WiFi or Ethernet)
- the sensors you like to use**DS18B20 sensors**, **relays**, **OLED display**, and **USB fans**

### 🔧 Setup Your Pi
Start with a cleaned Raspberry Pi. This project is tested on RPi 3, 4 and 5, but is expected to wok on other RPIs as well.
Choose the OS (64 bit recommended).
**BEFORE** your flash the RPi, go to the OS Settings / Advanced Settings and set it up to something meaningful. Most importantly, add your WiFi!
Take a username that works for you (e.g. brewmaster) and a device name such as connected-brewery
Your settings should look something like this:
<PICTURES1-3>

Once all setup, connect to your RPi via SSH
```sh
   ssh brewmaster@connected-brewery.com
   ```
Enter your password and off you go!

1. **Update & Upgrade the system**
   ```sh
   sudo apt update && sudo apt upgrade -y
   ```
2. **Install required packages**
   ```sh
   sudo apt install python3 python3-pip git mosquitto mosquitto-clients -y
   pip3 install flask paho-mqtt RPi.GPIO
   ```


### Install Virtual Environment

To keep things clean or organized, setup a virtual environment (venv) on your RPi
```sh
sudo apt install python3-venv -y
python3 -m venv ~/fermentation-venv
source ~/fermentation-venv/bin/activate
pip install --break-system-packages flask paho-mqtt RPi.GPIO
```

Once completed, verify the installation was successful running:

```sh
python3 -c "import flask, paho.mqtt.client, RPi.GPIO; print('Success!')"
```

### Make Virtual Environment Persistent
To avoid having to manually start your venv every time you power up the RPi, make it persostent via

```sh
echo "source ~/fermentation-venv/bin/activate" >> ~/.bashrc
source ~/.bashrc
pip install --upgrade pip
pip install --break-system-packages flask paho-mqtt RPi.GPIO
pip list | grep -E 'flask|paho-mqtt|RPi.GPIO'
```


### Clone Repository
At this stage, you are ready to get the code:
Navigate into the folder you like to hold your program in. (e.g. 'cd Desktop') and run

```sh
git clone https://github.com/mirkohahn/hasabrewery-fermentation-chamber.git
cd hasabrewery-fermentation-chamber
```

## Project Structure

tree

### Configure `config.py`

## Usage

## MQTT Messages
### **Structure of MQTT Messages Sent by Controller**
Example:
```json
{
    "timestamp": "2025-02-05 18:52:35",
    "temp_ambient": 22.5,
    "temp_brew": 18.0,
    "temp_top": 19.2,
    "temp_bottom": 17.8,
    "status": {
        "status_message": "OK",
        "transmission_type": "wifi",
        "RSSI": -78,
        "firmware_version": "0.1.2"
    }
}
```
### **Structure of MQTT Messages to Control Chamber**
Example:
```json
{
    "fermentation": {
        "stages_numbers": 3,
        "schedule": [
            {
                "stage": "Primary",
                "temperature": {
                    "value": 18,
                    "unit": "Celsius"
                },
                "pressure": {
                    "value": 15,
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
        "name": "Test Brew"
    }
}
```



## Wiring & Hardware
### **Wiring Guide**

| **Component** | **BCM Pin** | **Physical Pin** | **Function** |
|--------------|------------|----------------|-------------|
| **Button**   | GPIO 16    | Pin 36        | Start/Stop Fermentation Chamber |
| **LED**      | GPIO 13    | Pin 33        | Indicator |
| **GND**      | GND        | Pin 34        | Ground |

### **Hardware Components**
- Raspberry Pi
- DS18B20 Temperature Sensors
- I2C OLED Display
- Relays
- Fans (USB-powered)

### **Pictures & Diagrams**
_(Include wiring diagrams and hardware setup images)_

LED Test Script


        PWR     CHAM    WIFI    MQTT    TEMP
GREEN   16      13      27      17      22
        []      []      []      []      []
RED     5       24      25      6       23
        
       
        1   R: PWR ON
            G: Ready
        2   R: ERR Start
            G: Ready
        3   R: No WiFi
            G: WiFi Connected
        4   R: Not Connected to MQTT Host
            G: MQTT Connected
        5   R: Trouble with 1 or more Sensors
            G: All Sensors Working


State: -> 1 + 2 Green -> Chamebr Ready

# Troubleshoot

deactivate
source ~/fermentation-venv/bin/activate




## Notes on Setup & Development


### Initialize Temperature Sensor
Check if enabled:
```sh
ls /sys/bus/w1/devices/
```
If not, manually enable:
```sh
sudo nano /boot/firmware/config.txt
```
Add to bottom:
```sh
dtoverlay=w1-gpio
```
Then reboot:
```sh
sudo reboot
```

### Initialize MQTT
Ensure broker is running, then test by subscribing and publishing:
```sh
mosquitto_pub -h 192.168.0.209 -t "/control/fermentation_chamber/controller/2B3C4D" -m "Test Command from Mac"
```

### Test Relays

### Enable I2C
Run:
```sh
sudo raspi-config
```
Enable I2C under **Interfacing Options**.

Check detection:
```sh
sudo i2cdetect -y 1
```

### Setup USB Power Control
```sh
sudo apt update
sudo apt install uhubctl
```
List available hubs & ports:
```sh
sudo uhubctl
```
Control ports:
```sh
sudo uhubctl -a off -l 1-1 -p PORT_NO
sudo uhubctl -a on -l 1-1 -p PORT_NO
```

### Auto Start `start_button.py`
Create a systemd service:
```sh
sudo nano /etc/systemd/system/start_button.service
```
Add the following:
```ini
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
```
Enable and start the service:
```sh
sudo systemctl daemon-reload
sudo systemctl enable start_button.service
sudo systemctl start start_button.service
```
Check status:
```sh
sudo systemctl status start_button.service
```
Stop manually:
```sh
sudo systemctl stop start_button.service
```

## Upcoming Features

## Contribution

## Support this Project

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Has A Brewery Ecosystem

