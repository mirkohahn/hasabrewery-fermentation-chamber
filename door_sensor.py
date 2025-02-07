import RPi.GPIO as GPIO
import sys
import os
import time

#TODO: extra thread vs Interrupt Flag?

# Ensure access to config.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

# Load door sensor pin from config
DOOR_SENSOR_PIN = config.CONFIG["DOOR_SENSOR_PIN"]

# Track if the door was opened
door_was_opened = False

def setup_door_sensor():
    """Initialize GPIO pin for the door sensor and set up an interrupt."""
    GPIO.setmode(GPIO.BCM)

    # Ensure previous settings are cleared
    GPIO.cleanup(DOOR_SENSOR_PIN)

    # Setup pin as input before adding event detection
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Add event detection only if not already set
    if not GPIO.event_detected(DOOR_SENSOR_PIN):
        GPIO.add_event_detect(DOOR_SENSOR_PIN, GPIO.BOTH, callback=door_callback, bouncetime=200)

    print("✅ Door sensor initialized.")

def door_callback(channel):
    """Callback function triggered when the door state changes."""
    global door_was_opened
    if GPIO.input(DOOR_SENSOR_PIN) == GPIO.HIGH:
        print("🚪 Door Opened!")
        door_was_opened = True
    else:
        print("✅ Door Closed")

def get_door_status():
    """Returns 1 if the door was opened and resets flag, otherwise returns 0."""
    global door_was_opened
    if door_was_opened:
        door_was_opened = False
        return 1
    return 0

if __name__ == "__main__":
    try:
        setup_door_sensor()
        print("🔧 Door Sensor System Ready. Press CTRL+C to stop.")
        while True:
            print(f"Door Status: {get_door_status()}")
            time.sleep(0.250)  # Check every 250ms
    except KeyboardInterrupt:
        print("\n❌ Exiting...")
    finally:
        GPIO.cleanup()
