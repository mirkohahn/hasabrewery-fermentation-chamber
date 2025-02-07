import os
import csv
import time
from datetime import datetime
import config
import mqtt_subscriber

def get_log_file():
    """Retrieve the correct log file name based on the recipe name from state.json."""
    state_data = mqtt_subscriber.load_persistent_data()
    recipe_name = state_data.get("recipe_data", {}).get("name", "default").replace(" ", "_")
    return f"data/{recipe_name}_fermentation_log.csv"

# Buffer to hold log entries before writing
log_buffer = []
BUFFER_SIZE = 1



def log_data(temp_data, goal_brew_temp, cooler_on, heater_on, fan_on, stage_name):
    """Log temperature and control status to CSV file in chunks of 5 rows."""
    global log_buffer
    log_file = get_log_file()
    file_exists = os.path.isfile(log_file)

   

    # Append new data to the buffer
    log_buffer.append([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        f"{goal_brew_temp:.2f}",
        f"{temp_data['temp_brew']:.2f}",
        f"{temp_data['temp_ambient']:.2f}",
        f"{temp_data['temp_top']:.2f}",
        f"{temp_data['temp_bottom']:.2f}",
        int(cooler_on),
        int(heater_on),
        int(fan_on),
        stage_name
    ])

    # Write to file when buffer reaches the defined size
    if len(log_buffer) >= BUFFER_SIZE:
        with open(log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["timestamp", "goal_brew_temp", "brew_temp", "ambient_temp", "top_temp", "bottom_temp", "cooler_on", "heater_on", "fan_on", "stage_name"])
            
            writer.writerows(log_buffer)
            log_buffer.clear()  # Clear buffer after writing
    
    time.sleep(config.CONFIG["LOG_INTERVALL_LENGTH"])
