#!/usr/bin/python
import paho.mqtt.client as mqtt
from geometry_msgs.msg import PoseStamped
from mqtt2ros.msg import mqtt_msg
import rospy
import ssl

host = "mqtt.cloud.pozyxlabs.com"
port = 443
topic = "5f928c413528d3055d3093e5"
username = "5f928c413528d3055d3093e5"
password = "920a09b0-c5c6-4210-9e4c-60a0d0dff352"

ERROR = 54321
mqtt_pub = rospy.Publisher('mqtt_coord', mqtt_msg, queue_size= 1)

def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))

# callback triggered by a new Pozyx data packet
def on_message(client, userdata, msg):
    # print("Positioning update:", msg.payload.decode())

    poses = mqtt_msg()
    true = "True"
    false = "False"    

    ini_msg = eval(msg.payload.decode().encode('utf-8'))

    for i in ini_msg:
        pose = PoseStamped()
        dic_msg = str(i)
        if dic_msg.find('coordinates') != -1:
            dic_msg = eval(str(i))
            pose.header.seq = int(dic_msg['timestamp'])
            pose.header.stamp = rospy.get_rostime()
            pose.header.frame_id = dic_msg['tagId']
            pose.pose.position.x = dic_msg['data']['coordinates']['x']
            pose.pose.position.y = dic_msg['data']['coordinates']['y']
            pose.pose.position.z = dic_msg['data']['coordinates']['z']
            pose.pose.orientation.x = -1 * dic_msg['data']['tagData']['eulerAngles']['z']
            pose.pose.orientation.y = -1 * dic_msg['data']['tagData']['eulerAngles']['y']
            pose.pose.orientation.z = 360 - dic_msg['data']['tagData']['eulerAngles']['x']
            poses.data.append(pose)
        else:
            print("no coordinate ouputs")
            # pose.pose.position.x = pose.pose.position.y = pose.pose.position.z = ERROR
        
    if(pose.pose.position.x != ERROR or pose.pose.position.y != ERROR or pose.pose.position.z != ERROR):
        mqtt_pub.publish(poses)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")

def main():

    rospy.init_node("mqtt_local_api_node", anonymous=True)

    client = mqtt.Client(transport="websockets")
    client.username_pw_set(username, password=password)
    # sets the secure context, enabling the WSS protocol
    client.tls_set_context(context=ssl.create_default_context())
    # set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.connect(host, port=port)
    client.subscribe(topic)

    # works blocking, other, non-blocking, clients are available too.
    client.loop_forever()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
