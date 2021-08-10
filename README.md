# mqtt2ros
from mqtt IOT protocol (json) to ros msgs (rostopic)

## pozyx mqtt api protocol
https://docs.pozyx.io/enterprise/latest/interfaces/mqtt-api

## Requirements

```
sudo apt install mosquitto mosquitto-clients
pip install paho-mqtt or  python -m pip install paho-mqtt
pip install mqtt-recorder
```

## Run the Package
### Custom data pub/sub
```
# MQTT JSON publisher
python mqtt_json_pub.py ../data/config.json

# MQTT JSON Subscriber
python mqtt_json_sub.py
```
### Record/Replay MQTT data
```
# MQTT JSON record
mqtt-recorder --host [Gateway HOST IP] --mode record --file logs/filename.csv

# MQTT JSON replay
mqtt-recorder --host localhost --mode replay --file logs/filename.csv

# Rosbag replay
rosbag play logs/filename.bag
```
### Data sub2ros
```
# MQTT JSON Subscribe and Parse to custom ROS msg
rosrun mqtt2ros mqtt2rosmsg.py
```
## References
* https://stackoverflow.com/questions/42731998/how-to-publish-json-data-on-mqtt-broker-in-python
* https://gist.github.com/marianoguerra/be216a581ef7bc23673f501fdea0e15a
* https://rfriend.tistory.com/474
* http://www.steves-internet-guide.com/send-json-data-mqtt-python/
* https://pypi.org/project/mqtt-recorder/
