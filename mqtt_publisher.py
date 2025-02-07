import paho.mqtt.client as mqtt
import json
import config
import subprocess
from datetime import datetime
import control_logic
import fan_control

PUBLISH_TOPIC = f"/receive/{config.CONFIG['LOGIC_BREWERY_COMPONENT']}/{config.CONFIG['DEVICE_TYPE']}/{config.CONFIG['DEVICE_ID']}"

def get_rssi():
    """Retrieve the WiFi signal strength (RSSI)."""
    try:
        result = subprocess.run(["iwconfig", "wlan0"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "Signal level" in line:
                return int(line.split("Signal level=")[-1].split(" dBm")[0])
    except Exception as e:
        print(f"Error retrieving RSSI: {e}")
    return -100  # Default RSSI if error

def publish_status(temp_data, control_status):
    """Publish fermentation chamber status to MQTT."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(config.CONFIG["MQTT_BROKER"], config.CONFIG["MQTT_PORT"], 60)

    # Get additional data
    goal_brew_temp = control_logic.get_goal_brew_temp()
    fan_status = fan_control.get_fan_status()
    goal_chamber_temperature = control_logic.goal_chamber_temperature  # From global variable

    payload = json.dumps({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temp_ambient": temp_data["temp_ambient"],
        "temp_brew": temp_data["temp_brew"],
        "temp_top": temp_data["temp_top"],
        "temp_bottom": temp_data["temp_bottom"],
        "goal_brew_temp": goal_brew_temp,
        "goal_chamber_temperature": goal_chamber_temperature,
        "heater": control_status["heater"],
        "cooler": control_status["cooler"],
        "fan": fan_status,
        "status": {
            "status_message": "OK",
            "transmission_type": config.CONFIG["TRANSMISSION_TYPE"],
            "RSSI": get_rssi(),
            "firmware_version": config.CONFIG["FIRMWARE_VERSION"]
        }
    })

    client.publish(PUBLISH_TOPIC, payload)
    client.disconnect()
