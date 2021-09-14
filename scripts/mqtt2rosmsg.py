#!/usr/bin/python
import paho.mqtt.client as mqtt
from geometry_msgs.msg import PoseStamped
from mqtt2ros.msg import mqtt_msg
import rospy

host = "192.168.0.31" # fill in the IP of your gateway
topic = "tags"
port = 1883

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
            coor_x = dic_msg['data']['coordinates']['x']
            coor_y = dic_msg['data']['coordinates']['y']
            coor_z = dic_msg['data']['coordinates']['z']
            timestamp = dic_msg['timestamp']
            tag_id = dic_msg['tagId']

            pose.pose.position.x = coor_x
            pose.pose.position.y = coor_y
            pose.pose.position.z = coor_z
            pose.header.seq = int(timestamp)
            pose.header.frame_id = tag_id

        else:
            print("no coordinate ouputs")
            pose.pose.position.x = pose.pose.position.y = pose.pose.position.z = ERROR
        
        poses.data.append(pose)

    if(pose.pose.position.x != ERROR or pose.pose.position.y != ERROR or pose.pose.position.z != ERROR):
        mqtt_pub.publish(poses)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")

def main():

    rospy.init_node("mqtt_local_api_node", anonymous=True)

    client = mqtt.Client()
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
