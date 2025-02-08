import os

CONFIG = {
"FIRMWARE_VERSION":"0.7.0",                         # do not change - will be changed in main branch
    # Missing to V1.0:
        
        # V0.8 DOOR SENSOR, 
        # V0.9 IMPERIAL UNITS, 
        # V1.0 FINAL TEST & IMPROVEMENTS
        
    "TRANSMISSION_TYPE": "wifi",                    # Potentially adding BLE and/or Zigbee
    
# <--- M Q T T   S E T U P   &   S T R U C T U R E --->
    # "MQTT_BROKER": "your.host.ip",                 # Replace with your broker IP/hostname
    "MQTT_BROKER": "192.168.0.209",                 # Replace with your broker IP/hostname
    "MQTT_PORT": 1883,                              # Default MQTT port; change if needed
    
    "LOGIC_BREWERY_COMPONENT": "fermentation_chamber",
    "DEVICE_TYPE": "controller",
    "DEVICE_ID": "2B3C4D",                          # Replace with your device ID; Reocmmended: Random 6-digit hex
    
    "INTERVAL_LENGTH": 10,                          # transmits an mqtt message roughly every [x] seconds

# <--- L O G F I L E & D A T A   S T O R A G E --->
    "DATA_STORAGE_FILE": "data/state.json",         
    "LOG_INTERVALL_LENGTH": 10,                      # write to csv log every [x] seconds


# <--- T H E R M O M E T E R   D S 1 8 B 2 0 --->    
    "ID_THERMOMETER": [1, 2, 3, 4],                 # do not change - internal use only
    
    #IMPERIAL NOT YET WORKING
    "IMPERIAL_UNITS": False,                        # set True if setup uses imperial (°F) over °C & metric system
    
    # DS18B20 Sensor Assignments
    "TEMP_AMBIENT": "28-030a9794268a",              # add your DS18B20 IDs (e.g. 28-123456789abc)
    "TEMP_TOP": "28-3c1f04579aa4",                  # for each thermometer add the specific ID
    "TEMP_BOTTOM": "28-03139497584a",               # run /tests/test_sensors.py to identify connected thermometers
    "TEMP_BREW": "28-030594973474",


# <--- R E L A Y   S E T U P --->
    "HEATER_CONNECTED": True,
    "COOLER_CONNECTED": True,
    "RELAY_PINS": {
        "heater": 26,                                # Change to GPIO Pin used for each relay; default: 26 (Pin 37)
        "cooler": 20,                                # Default: GPIO 20 (Pin 38)
        "Relay 3": 21                                # Default: GPIO 21 (Pin 40) | Current NOT in use
    },

# <--- F A N   C O N T R O L L E R --->
    "FAN_USB_PORT_NO":2,                            # USB Fan, Controller turn OFF USB Port w/ no [x]
    
# <--- S E T U P   D O O R   S E N S O R --->    
    "DOOR_SENSOR_PIN":16,                           # Choose GPIO Pin used for door sensor; Default: GPIO 16 
    
# <--- CONTROLLER CUSTOMIZATION --->
    # FYI: all temps in unit set above; Default °C
    # GENERAL TEMP THRESHOLDS
    "MINIMIM_CHAMBER_TEMP": -5,                     # Set ABSOLUTE Min Temp for Brew & Chamber
    "MINIMIM_BREW_TEMP": 0.75,                      # PROTECT beer from freezing
    
    # FAN CONTROLLER
    "CHAMBER_TEMP_DIFFERENCE_MAX": 2,               # Turns Fans ON@MAX and OFF@MIN
    "CHAMBER_TEMP_DIFFERENCE_MIN": 0.5,
    
    # ADJUST TOLERANCES
    "BREW_TEMP_EXCEED": 0.5,                        # Allow Beer Temp to exceed Goal_Temp by [x] before taking action (aka. cooling)
    "BREW_TEMP_UNDERSHOOT": 1,                      # Allow Beer Temp to be below Goal_Temp by [x] before taking action (aka heating)
    "CHAMBER_TEMP_IDLE_RANGE": 2,                   # Add Buffer or Idle Zone to Temp in Chamber for Efficiency | +/- to either side
    

# <--- A D V A N C E D   S E T T I N G S --->
    # PID CONTROLLER CALIBRATIONS                   # Currently only P (out of PID) implemented; rest coming soon after field test
    # PROPORTIONAL
    "INTENSITY_FACTOR": -1.0,                       # Adjust proportional temp correction
    
    # INTEGRATED                                    # Coming soon
    
    # DERIVATIVE                                    # Coming soon
    
}