import RPi.GPIO as GPIO

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering

# Define LED GPIO pins
LED_PINS = {
    "power_red": 5,
    "power_green": 16,
    # "chamber_red": 24,
    # "chamber_green": 13,
    "wifi_red": 25,
    "wifi_green": 27,
    "mqtt_red": 6,
    "mqtt_green": 17,
    "sensor_red": 23,
    "sensor_green": 22
}

# Initialize status flags
LED_STATUS = {led: False for led in LED_PINS}

# Set up GPIO pins as output and turn them off initially
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Functions to turn on each LED and upddate status flag
def turn_on_power_red():
    GPIO.output(LED_PINS["power_red"], GPIO.HIGH)
    LED_STATUS["power_red"] = True
    print("🟥 [1] - Power LED - Board has Power")

def turn_on_power_green():
    GPIO.output(LED_PINS["power_green"], GPIO.HIGH)
    GPIO.output(LED_PINS["power_red"], GPIO.LOW)
    LED_STATUS["power_green"] = True
    LED_STATUS["power_red"] = False
    print("🟩 [1] - Power LED - Boot Completed - Ready for Use")



# def turn_on_chamber_red():
#     GPIO.output(LED_PINS["chamber_red"], GPIO.HIGH)
#     LED_STATUS["chamber_red"] = True
#     print("🟥 [2] - Chamber LED - Error with Has A Brewery Controller")

# def turn_on_chamber_green():
#     GPIO.output(LED_PINS["chamber_green"], GPIO.HIGH)
#     LED_STATUS["chamber_green"] = True
#     print("🟩 [2] - Chamber LED - Has A Brewery Controller Started & Ready")

def turn_on_wifi_red():
    GPIO.output(LED_PINS["wifi_red"], GPIO.HIGH)
    LED_STATUS["wifi_red"] = True
    GPIO.output(LED_PINS["wifi_green"], GPIO.LOW)
    LED_STATUS["wifi_green"] = False
    print("🟥 [3] - WiFi LED - Board has no WiFi Connection")

def turn_on_wifi_green():
    GPIO.output(LED_PINS["wifi_green"], GPIO.HIGH)
    LED_STATUS["wifi_green"] = True
    GPIO.output(LED_PINS["wifi_red"], GPIO.LOW)
    LED_STATUS["wifi_red"] = False
    print("🟩 [3] - WiFi LED - Connected to WiFi Network")

def turn_on_mqtt_red():
    GPIO.output(LED_PINS["mqtt_red"], GPIO.HIGH)
    LED_STATUS["mqtt_red"] = True
    print("🟥 [4] - MQTT LED - Not Connected to MQTT Host")

def turn_on_mqtt_green():
    GPIO.output(LED_PINS["mqtt_green"], GPIO.HIGH)
    GPIO.output(LED_PINS["mqtt_red"], GPIO.LOW)
    LED_STATUS["mqtt_green"] = True
    LED_STATUS["mqtt_red"] = False
    print("🟩 [4] - MQTT LED - Chamber connected to MQTT Host")

def turn_on_sensor_red():
    GPIO.output(LED_PINS["sensor_red"], GPIO.HIGH)
    GPIO.output(LED_PINS["sensor_green"], GPIO.LOW)
    LED_STATUS["sensor_red"] = True
    LED_STATUS["sensor_green"] = False
    print("🟥 [5] - Sensor LED - Issue with 1 or more Sensors")

def turn_on_sensor_green():
    GPIO.output(LED_PINS["sensor_green"], GPIO.HIGH)
    GPIO.output(LED_PINS["sensor_red"], GPIO.LOW)
    LED_STATUS["sensor_green"] = True
    LED_STATUS["sensor_red"] = False
    print("🟩 [5] - Power LED - No Issues with Sensors detected")

def cleanup():
    GPIO.cleanup()
