import sys
import os

# Add parent directory to sys.path so we can import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import paho.mqtt.client as mqtt
import time
import json
import config  # Now it should work!

# Get MQTT settings from config
MQTT_BROKER = config.CONFIG["MQTT_BROKER"]
MQTT_PORT = config.CONFIG["MQTT_PORT"]
LOGIC_BREWERY_COMPONENT = config.CONFIG["LOGIC_BREWERY_COMPONENT"]
DEVICE_TYPE = config.CONFIG["DEVICE_TYPE"]
DEVICE_ID = config.CONFIG["DEVICE_ID"]

PUBLISH_TOPIC = f"/receive/{LOGIC_BREWERY_COMPONENT}/{DEVICE_TYPE}/{DEVICE_ID}/"
SUBSCRIBE_TOPIC = f"/control/{LOGIC_BREWERY_COMPONENT}/{DEVICE_TYPE}/{DEVICE_ID}"

def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    print(f"Connected to MQTT Broker with code {rc}")
    client.subscribe(SUBSCRIBE_TOPIC)
    print(f"Subscribed to: {SUBSCRIBE_TOPIC}")

def on_message(client, userdata, msg):
    """Callback when message is received"""
    print(f"Received on {msg.topic}: {msg.payload.decode()}")

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

try:
    while True:
        payload = json.dumps({"message": "Hello From MQTT Test"})
        print(f"Publishing to {PUBLISH_TOPIC}: {payload}")
        client.publish(PUBLISH_TOPIC, payload)
        time.sleep(5)  # Send every 5 seconds
except KeyboardInterrupt:
    print("MQTT Test Stopped")
    client.loop_stop()
    client.disconnect()
