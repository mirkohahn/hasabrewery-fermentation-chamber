import RPi.GPIO as GPIO
import time
import os
import signal
import subprocess
import relay_control  # Import relay control module
import display
import fan_control
import led_status_handler as led

# Pin Definitions
BUTTON_PIN = 16  # GPIO 16 (Pin 36)
LED_PIN = 13  # GPIO 13 (Pin 33)

# Path to `main.py`
MAIN_SCRIPT = "/home/brewmaster/Desktop/hasabrewery-fermentation-chamber/main.py"

# Track process running `main.py`
process = None

def start():
    """Called when LED is turned ON. Starts main.py."""
    GPIO.setwarnings(False)

    global process
    if process is None:
        print("🚀 start() called, starting fermentation chamber (main.py)")
        process = subprocess.Popen(["python3", MAIN_SCRIPT], preexec_fn=os.setsid)  # ✅ Uses system Python (no venv restart)

def stop():
    """Called when LED is turned OFF. Stops main.py and shuts down relays."""
    global process
    GPIO.setwarnings(False)

    print("🌙 stop() called, stopping fermentation chamber and turning off relays")
    relay_control.turn_cooler_off()
    relay_control.turn_heater_off()
    fan_control.turn_fans_off()
    display.clear_display()  # Clear welcome message but keep display on

    if process:
        print("🛑 Stopping main.py gracefully...")
        GPIO.setwarnings(False)

        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process = None

def check_wifi():
    """Check if the Raspberry Pi is connected to WiFi and print status."""
    try:
        ssid = subprocess.check_output(["iwgetid", "-r"], text=True).strip()
        if ssid:
            print(f"✅ Connected to WiFi: {ssid}")
            led.turn_on_wifi_green()
            GPIO.setwarnings(False)

        else:
            print("❌ Not connected to any WiFi network.")
            GPIO.setwarnings(False)

            # led.turn_on_wifi_red()
    except subprocess.CalledProcessError:
        print("⚠️ Could not determine WiFi status (check if `iwgetid` is available).")
        GPIO.setwarnings(False)

        # led.turn_on_wifi_red()

def setup():
    """Initialize GPIO settings."""
    GPIO.setwarnings(False)  # Suppress warnings
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

    # Set up LED as output
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)  # Start with LED OFF

    # Set up Button as input with an internal pull-up resistor
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # led.turn_on_power_green()
    # led.turn_on_wifi_red()
    check_wifi()  # ✅ Call WiFi check before setup

    stop()

def loop():
    """Main loop to monitor button and control LED."""
    global process
    GPIO.setwarnings(False)

    led_state = False  # Tracks current LED state

    try:
        while True:
            button_pressed = GPIO.input(BUTTON_PIN) == GPIO.LOW
            GPIO.setwarnings(False)


            if button_pressed and not led_state:  # Button pressed, LED was OFF
                GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED ON
                led_state = True
                start()

            elif not button_pressed and led_state:  # Button released, LED was ON
                GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED OFF
                led_state = False
                stop()

            time.sleep(0.1)  # Small delay to debounce
    except KeyboardInterrupt:
        print("🔄 Exiting gracefully...")
        stop()  # Ensure everything is stopped before exit
        # led.cleanup()
        GPIO.cleanup()

if __name__ == "__main__":
    setup()
    loop()
