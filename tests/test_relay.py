import RPi.GPIO as GPIO
import time
import sys
import os

# Ensure parent directory is in sys.path to find config.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import config  # Import config after setting sys.path

# Load relay pins from config
RELAY_PINS = config.CONFIG["RELAY_PINS"]

def setup_relays():
    """Initialize GPIO pins for relays"""
    GPIO.setmode(GPIO.BCM)
    for pin in RELAY_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)  # Ensure all relays start OFF

def toggle_relay(relay_name, state):
    """Turn a relay ON or OFF"""
    pin = RELAY_PINS[relay_name]
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
    print(f"{'Turning on' if state else 'Turning off'} {relay_name}")

def main():
    """Loop through relays in sequence"""
    setup_relays()
    try:
        while True:
            toggle_relay("heater", True)
            time.sleep(1)

            toggle_relay("cooler", True)
            time.sleep(1)

            toggle_relay("Relay 3", True)
            time.sleep(5)

            print("Turning all off")
            for relay in RELAY_PINS:
                toggle_relay(relay, False)

            time.sleep(2)  # Pause before restarting loop

    except KeyboardInterrupt:
        print("\nStopping relay test...")
        GPIO.cleanup()  # Reset GPIO pins

if __name__ == "__main__":
    main()
