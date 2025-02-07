import RPi.GPIO as GPIO
import sys
import os
import time

# Ensure access to config.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

# Disable GPIO warnings
GPIO.setwarnings(False)

# Set GPIO mode
GPIO.setmode(GPIO.BCM)  # Ensure BCM mode is set before using GPIO pins

# Load relay pin mappings from config
RELAY_PINS = config.CONFIG.get("RELAY_PINS", {})

def setup_relays():
    """Initialize GPIO pins for all defined relays."""
    for relay, pin in RELAY_PINS.items():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)  # Ensure all relays start OFF
    print("✅ Relays initialized.")

def turn_cooler_on():
    # """Turn the cooler relay ON."""
    toggle_relay("heater", False)
    toggle_relay("cooler", True)

def turn_cooler_off():
    # """Turn the cooler relay OFF."""
    toggle_relay("cooler", False)

def turn_heater_on():
    # """Turn the heater relay ON."""
    toggle_relay("cooler", False)
    toggle_relay("heater", True)

def turn_heater_off():
    # """Turn the heater relay OFF."""
    toggle_relay("heater", False)

def toggle_relay(relay_name, state):
    # """Turn a relay ON or OFF based on its name from config.py."""
    if relay_name not in RELAY_PINS:
        print(f"⚠️ Warning: Relay '{relay_name}' is not defined in config.py!")
        return

    pin = RELAY_PINS[relay_name]
    GPIO.setup(pin, GPIO.OUT)  # Ensure pin is configured as output
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
    # print(f"{'✅ Turning ON' if state else '⛔ Turning OFF'} {relay_name} (GPIO {pin})")

def get_relay_status(relay_name):
    # """Returns 1 if the relay is ON, 0 if OFF. Supports 'heater' and 'cooler'."""
    if relay_name not in ["heater", "cooler"]:
        print(f"⚠️ Error: Invalid relay name '{relay_name}'. Use 'heater' or 'cooler'.")
        return 0

    if relay_name in RELAY_PINS:
        pin = RELAY_PINS[relay_name]
        GPIO.setup(pin, GPIO.OUT)  # Ensure the pin is configured as output before reading
        return 1 if GPIO.input(pin) == GPIO.HIGH else 0

    print(f"⚠️ Error: Relay '{relay_name}' is not defined in config.py!")
    return 0

def all_off():
    # """Turn off all relays."""
    for relay in RELAY_PINS:
        toggle_relay(relay, False)

if __name__ == "__main__":
    setup_relays()
    
    # Step 1: Turn everything off
    all_off()
    # print("All relays OFF.")
    
    # Step 2: Test cooler
    input("Next: turning on cooler. Press Enter to continue...")
    turn_cooler_on()
    # print(f"Cooler status: {get_relay_status('cooler')}")
    input("Next: turning off cooler. Press Enter to continue...")
    turn_cooler_off()
    # print(f"Cooler status: {get_relay_status('cooler')}")

    # Step 3: Test heater
    input("Next: turning on heater. Press Enter to continue...")
    turn_heater_on()
    # print(f"Heater status: {get_relay_status('heater')}")
    input("Next: turning off heater. Press Enter to continue...")
    turn_heater_off()
    # print(f"Heater status: {get_relay_status('heater')}")

    # Step 4: Turn everything off again
    all_off()
    # print("All off. Test complete.")
