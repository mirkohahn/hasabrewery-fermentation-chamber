import time
import json
import threading
import os
import sys

# Ensure access to other modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import config
import sensors
import relay_control
import display
import mqtt_publisher
import mqtt_subscriber
import control_logic
import log_handler
import fan_control

# Global variable for MQTT interval tracking
last_mqtt_time = time.time()

def initialization_sequence():
    # """Run system initialization: Welcome message, relays off, turn cooler ON."""
    # print("🚀 Starting fermentation chamber controller...")

    # 1️⃣ Initialize and show welcome message
    display.init_display()
    display.show_text(f"Welcome\nFirmware: {config.CONFIG['FIRMWARE_VERSION']}")
   
    # 2️⃣ Ensure all relays are OFF, then turn cooler ON
    relay_control.setup_relays()
    relay_control.toggle_relay("heater", False)  # Ensure heater is OFF
    relay_control.toggle_relay("cooler", False)  # Turn cooler ON
    
    time.sleep(5)
    display.clear_display()  # Clear welcome message but keep display on

def main_loop():
    # """Main operation loop for temperature control, logging, and MQTT updates."""
    global last_mqtt_time

    while True:
        loop_start_time = time.time()
        

        # 1️⃣ Get temperature readings
        temp_data = sensors.read_all_temperatures()

        # 2️⃣ Determine control actions based on temperature
        control_status = control_logic.evaluate(temp_data)

        # 3️⃣ Get control states
        goal_brew_temp = control_logic.get_goal_brew_temp()
        stage_name = control_logic.get_stage_name()
        brew_temp = temp_data.get("temp_brew", "N/A")  # Prevent crashes if key missing
        cooler_on = relay_control.get_relay_status("cooler")
        heater_on = relay_control.get_relay_status("heater")
        fan_on = fan_control.get_fan_status()

        # 4️⃣ Update the display only (without clearing or blinking)
        display.show_text(f"Goal Temp: {goal_brew_temp}\nBrew Temp: {brew_temp}")

        # print(f"Goal Brew Temp: {goal_brew_temp} | Cooler: {cooler_on} | Heater: {heater_on} | Fan: {fan_on}")

        # 5️⃣ Pass data to logging handler
        log_handler.log_data(temp_data, goal_brew_temp, cooler_on, heater_on, fan_on, stage_name)

        # 6️⃣ Send MQTT message every INTERVAL_LENGTH seconds
        if time.time() - last_mqtt_time >= config.CONFIG["INTERVAL_LENGTH"]:
            mqtt_publisher.publish_status(temp_data, control_status)
            last_mqtt_time = time.time()

        # 7️⃣ Maintain loop timing (1-second intervals)
        loop_duration = time.time() - loop_start_time
        if loop_duration < config.CONFIG['LOG_INTERVALL_LENGTH']:
            time.sleep(config.CONFIG['LOG_INTERVALL_LENGTH'] - loop_duration)
        print(loop_duration)

if __name__ == "__main__":
    initialization_sequence()

    # Start MQTT subscriber in a separate thread
    mqtt_thread = threading.Thread(target=mqtt_subscriber.start_mqtt_subscriber, daemon=True)
    mqtt_thread.start()

    # Start main loop
    main_loop()
