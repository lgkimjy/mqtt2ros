# mqtt2ros
from mqtt IOT protocol (json) to ros msgs (rostopic)

## pozyx mqtt api protocol
https://docs.pozyx.io/enterprise/latest/interfaces/mqtt-api

## Requirements

```
sudo apt install mosquitto mosquitto-clients
pip install paho-mqtt or  python -m pip install paho-mqtt
```


## Run the Package
```
# MQTT JSON publisher
python mqtt_json_pub.py ../data/config.json

# MQTT JSON Subscriber
python mqtt_json_sub.py
```