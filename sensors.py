import os
import time
import sys
import led_status_handler as led


# Ensure access to config.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

# Enable DS18B20 sensors on Raspberry Pi
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

SENSOR_PATH = "/sys/bus/w1/devices/"

def read_temperature(sensor_id):
    """Read temperature from a specific DS18B20 sensor."""
    if not sensor_id:
        # led.turn_on_sensor_red()
        return -99.99  # Return default value if sensor ID is missing

    device_file = f"{SENSOR_PATH}{sensor_id}/w1_slave"

    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()

        if "YES" not in lines[0]:  # Sensor data is not valid
            print(f"⚠️ Warning: Sensor {sensor_id} returned invalid data.")
            # led.turn_on_sensor_red()
            return -99.99

        temp_string = lines[1].split("t=")[-1]
        return round(float(temp_string) / 1000.0, 2)  # Temperature in Celsius
    except FileNotFoundError:
        print(f"❌ Error: Sensor {sensor_id} not found. Returning -99.99°C.")
        # led.turn_on_sensor_red()
        return -99.99
    except Exception as e:
        print(f"❌ Unexpected error reading sensor {sensor_id}: {e}")
        # led.turn_on_sensor_red()
        return -99.99

def read_all_temperatures():
    """Read all four temperatures using assigned sensor IDs from config.py."""
    return {
        "temp_ambient": read_temperature(config.CONFIG.get("TEMP_AMBIENT", "")),
        "temp_top": read_temperature(config.CONFIG.get("TEMP_TOP", "")),
        "temp_bottom": read_temperature(config.CONFIG.get("TEMP_BOTTOM", "")),
        "temp_brew": read_temperature(config.CONFIG.get("TEMP_BREW", ""))
    }

if __name__ == "__main__":
    print("🔍 Reading DS18B20 sensors...")
    temperatures = read_all_temperatures()
    print(temperatures)
