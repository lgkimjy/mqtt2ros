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
### Custom data pub/sub
```
# MQTT JSON publisher
python mqtt_json_pub.py ../data/config.json

# MQTT JSON Subscriber
python mqtt_json_sub.py
```
### Logging MQTT data
```
# Use it like rosbag

```
### Log data pub/sub2ros
```
# MQTT JSON log data publisher
python mqtt_json_pub.py ../log/log.json

# MQTT JSON Subscribe and Parse to custom ROS msg
rosrun mqtt2ros mqtt2rosmsg.py
```
## References
* https://stackoverflow.com/questions/42731998/how-to-publish-json-data-on-mqtt-broker-in-python
* https://gist.github.com/marianoguerra/be216a581ef7bc23673f501fdea0e15a
* https://rfriend.tistory.com/474
* http://www.steves-internet-guide.com/send-json-data-mqtt-python/
