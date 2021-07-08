#!/usr/bin/python
from geometry_msgs.msg import PoseStamped
from mqtt2ros.msg import mqtt_msg
import bridge
import rospy
import signal

MQTT_TOPIC = 'uwb'
MQTT_HOST = 'localhost'
MQTT_CLIENT_ID = 'bridge'
MQTT_PORT = '1883'

class mqtt_bridge(bridge.bridge):

    def msg_process(self, msg):

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

                poses.data.append(pose)
        mqtt_pub = rospy.Publisher('mqtt', mqtt_msg, queue_size= 1)
        mqtt_pub.publish(poses)


def main():
    rospy.init_node('mqtt_2_ros', anonymous=True) 
    mqtt_sub = mqtt_bridge(MQTT_TOPIC, MQTT_CLIENT_ID, MQTT_HOST, MQTT_PORT)
    rospy.on_shutdown(mqtt_sub.hook)
    while not rospy.is_shutdown():
        mqtt_sub.looping()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
