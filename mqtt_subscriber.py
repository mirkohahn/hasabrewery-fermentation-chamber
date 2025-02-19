import os
import sys
import json
import paho.mqtt.client as mqtt
from threading import Lock
import led_status_handler as led


# Ensure the parent directory is accessible
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import config

# Constants
SUBSCRIBE_TOPIC = f"/control/{config.CONFIG['LOGIC_BREWERY_COMPONENT']}/{config.CONFIG['DEVICE_TYPE']}/{config.CONFIG['DEVICE_ID']}"
DATA_FILE = config.CONFIG["DATA_STORAGE_FILE"]
LOCK = Lock()  # Thread-safe handling

def load_persistent_data():
    """ Load persistent data from file """
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: Corrupted JSON file, starting fresh.")
        return {}

def save_persistent_data(data):
    """ Save persistent data to file """
    with LOCK:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

def update_fermentation_data(new_data):
    """ Update stored fermentation data with incoming MQTT data """
    current_data = load_persistent_data()

    # Merge new values while preserving existing ones
    for key, value in new_data.items():
        if isinstance(value, dict) and key in current_data:
            current_data[key].update(value)
        else:
            current_data[key] = value

    save_persistent_data(current_data)
    print("Updated fermentation data:", json.dumps(current_data, indent=4))

def on_connect(client, userdata, flags, rc, properties):
    """ Callback when connecting to MQTT broker """
    if rc == 0:
        print(f"Connected to MQTT Broker: {config.CONFIG['MQTT_BROKER']}")
        # led.turn_on_mqtt_green()
        client.subscribe(SUBSCRIBE_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    """ Callback when receiving an MQTT message """
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Received on {msg.topic}: {json.dumps(payload, indent=4)}")
        update_fermentation_data(payload)
    except json.JSONDecodeError:
        print(f"Invalid JSON received on {msg.topic}")

def start_mqtt_subscriber():
    """ Initialize MQTT client and start listening """
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config.CONFIG["MQTT_BROKER"], config.CONFIG["MQTT_PORT"], 60)
    client.loop_start()  # Run in the background

if __name__ == "__main__":
    start_mqtt_subscriber()
