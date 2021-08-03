import paho.mqtt.client as mqtt
import ssl
import sys

# how to use :
# python mqtt_json_record.py ../logs/filename.json
# after finsih the nodes, go to filename.json and ctrl+shift+i to
# re-align the json file.


host = "10.0.0.254" # fill in the IP of your gateway
port = 1883
topic = "tags" 

args = sys.argv[1]
f = open(args, "w")
f.close()

def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))

# callback triggered by a new Pozyx data packet
def on_message(client, userdata, msg):
    # print("Positioning update:", msg.payload.decode())
    # f = open("../logs/log.json")
    with open(args, 'a') as f:
        f.write(msg.payload.decode())
        f.close()
    # print(msg.topic)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")

client = mqtt.Client()

# set callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(host, port=port)
client.subscribe(topic)

# works blocking, other, non-blocking, clients are available too.
client.loop_forever()