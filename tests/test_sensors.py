import os
import glob
import time

# Load kernel modules for 1-Wire support
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

SENSOR_PATH = "/sys/bus/w1/devices/"

def get_sensors():
    """Detect connected DS18B20 sensors"""
    return [sensor.split('/')[-1] for sensor in glob.glob(SENSOR_PATH + "28*")]

def read_temperature(sensor_id):
    """Read temperature from a specific DS18B20 sensor"""
    device_file = f"{SENSOR_PATH}{sensor_id}/w1_slave"
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        if "YES" not in lines[0]:
            return None
        temp_string = lines[1].split("t=")[-1]
        return float(temp_string) / 1000.0
    except Exception as e:
        print(f"Error reading sensor {sensor_id}: {e}")
        return None

if __name__ == "__main__":
    print("Detecting DS18B20 sensors...")
    sensors = get_sensors()

    if not sensors:
        print("No DS18B20 sensors detected! Check wiring.")
    else:
        print(f"Found {len(sensors)} sensor(s): {sensors}")
        for sensor in sensors:
            temp = read_temperature(sensor)
            if temp is not None:
                print(f"Sensor {sensor}: {temp:.2f}°C")
            else:
                print(f"Sensor {sensor}: Error reading temperature")
