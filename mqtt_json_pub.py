#!/usr/bin/env python
import paho.mqtt.client as mqtt
import json
import time
import sys

# Define Variables
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "uwb"

# JSON file input parsing
file_path = sys.argv[1]
with open(file_path) as json_file:
    json_data = json.load(json_file)
    MQTT_MSG=json.dumps(json_data)

# Define on_publish event function
def on_publish(client, userdata, mid):
    print("Message Publishing...")

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)
    client.publish(MQTT_TOPIC, MQTT_MSG)

def on_message(client, userdata, msg):
    # print(msg.topic)
    # print(msg.payload)
    payload = json.loads(msg.payload)    # you can use json.loads to convert string to json
    client.disconnect()                  # Got message then disconnect

def main():
    # Initiate MQTT Client
    mqttc = mqtt.Client()

    # Register publish callback function
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    while True:
        # Connect with MQTT Broker
        mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
        # Loop forever
        mqttc.loop_forever()
        time.sleep(0.1)

if __name__ == '__main__':
    main()