# 🍺 HasABrewery Fermentation Chamber | Full Control - Plug & Play
[![Version](https://img.shields.io/badge/version-1.0.1-brightgreen)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)  
[![Platform](https://img.shields.io/badge/platform-ESP32-orange)](https://espressif.com/)

## 🚀 ChEAPER THAN INKBIRD & Fully Connected
The Fermentation Chamber Controller is a Raspberry Pi-based system for automating temperature control in fermentation. 
It integrates **DS18B20 sensors**, **MQTT communication**, **relay control**, and an **OLED display**. This project 
ensures optimal fermentation conditions, supports remote monitoring, and is part of the **Has A Brewery Ecosystem**.



## 🔍 Overview
This project provides an automated and remote-controlled fermentation chamber to ensure optimal brewing conditions. The system integrates sensors, relays, and a Raspberry Pi to control and monitor temperature during fermentation.

## 🏗️ Platform


## 🛠️ Installation
### 📋 Prerequisites
Ensure you have:
- A **Raspberry Pi** (any model with GPIO support)
- An **SD card** with Raspberry Pi OS installed
- **Internet connection** (WiFi or Ethernet)
- **DS18B20 sensors**, **relays**, **OLED display**, and **USB fans**



### 📥 Clone Repository
```sh
git clone <HTTPS-REPOSITORY-URL>
cd hasabrewery-fermentation-chamber
```

### ⚙️ Configure `config.py`
Edit the `config.py` file to match your setup.

## 🏭 Usage
Run the program with:
```sh
python3 start_button.py
```
Press the physical button to start/stop the chamber.

## 📡 MQTT Messages
### 📤 **MQTT Messages Sent by Controller**
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
### 📥 **MQTT Messages to Control Chamber**
```json
{
    "fermentation": {
        "stages_numbers": 3,
        "schedule": [
            {
                "stage": "Other Stage",
                "temperature": {
                    "value": 40,
                    "unit": "Celsius"
                }
            }
        ]
    },
    "recipe_data": {
        "id": "ABC123",
        "name": "Test Brew3"
    }
}
```

## 📂 Project Structure
_(Detailed breakdown of files and directories)_

## 🔌 Wiring & Hardware
### 🔧 **Wiring Guide**
| **Component** | **BCM Pin** | **Physical Pin** | **Function** |
|--------------|------------|----------------|-------------|
| **Button**   | GPIO 16    | Pin 36        | Start/Stop Fermentation Chamber |
| **LED**      | GPIO 13    | Pin 33        | Indicator |
| **GND**      | GND        | Pin 34        | Ground |

### 🏗️ **Hardware Components**
- Raspberry Pi
- DS18B20 Temperature Sensors
- I2C OLED Display
- Relays
- USB-powered Fans

### 📸 **Pictures & Diagrams**
![Wiring Diagram](path/to/image.png)

## 🛠️ Setup & Development Notes
### 🔬 Enable I2C
```sh
sudo raspi-config
```
Enable I2C under **Interfacing Options**.
```sh
sudo i2cdetect -y 1
```

### 🔄 Auto Start `start_button.py`
```sh
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

## 🌟 Upcoming Features
- 📊 Web-based monitoring dashboard
- 🔗 Integration with cloud services

## 🤝 Contribution
Pull requests are welcome! Follow the [contribution guidelines](CONTRIBUTING.md).

## 💖 Support This Project
Consider starring ⭐ this repository and sharing it with others in the brewing community!

## 📜 License
This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## 🍻 Has A Brewery Ecosystem
Part of a larger ecosystem for connected brewing automation. Stay tuned for more!

---

✅ **Now enriched with emojis, placeholders for images, and complete sentences.** 🚀 Let me know if any refinements are needed!

