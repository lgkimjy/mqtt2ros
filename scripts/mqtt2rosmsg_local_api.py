#!/usr/bin/python3
import paho.mqtt.client as mqtt
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import MagneticField, Imu
from mqtt2ros.msg import mqtt_msg, mqtt_mag, mqtt_imu
import rospy
import ssl
import signal, sys

host = "10.0.0.254"   # "192.168.50.201" # fill in the IP of your gateway
topic = "tags"
port = 1883

ERROR = 54321
count = 0
id_checker = []

mqtt_pose_pub = rospy.Publisher('mqtt_coord', mqtt_msg, queue_size= 1)
mqtt_mag_pub  = rospy.Publisher('mqtt_mag', mqtt_mag, queue_size= 1)
mqtt_imu_pub  = rospy.Publisher('mqtt_imu', mqtt_imu, queue_size=1)

poses = mqtt_msg()
mags = mqtt_mag()
imus = mqtt_imu()

def signal_handler(sig, frame):
    print('Keyboard Ctrl+C! interrupted')
    sys.exit(0)

def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))

# callback triggered by a new Pozyx data packet
def on_message(client, userdata, msg):
    global count
    # print("Positioning update:", msg.payload.decode())

    true = "True"
    false = "False"
    null = "None"

    ini_msg = eval(msg.payload.decode().encode('utf-8'))

    for i in ini_msg:
        pose = PoseStamped()
        mag = MagneticField()
        imu = Imu()
        dic_msg = str(i)
        if dic_msg.find('coordinates') != -1:
            dic_msg = eval(str(i))
            pose.header.seq = int(dic_msg['timestamp'])
            mag.header.seq = int(dic_msg['timestamp'])
            
            imu.header.stamp = mag.header.stamp = pose.header.stamp = rospy.get_rostime()
            pose.header.frame_id = mag.header.frame_id = imu.header.frame_id = dic_msg['tagId']
            
            # pose
            pose.pose.position.x = dic_msg['data']['coordinates']['x']
            pose.pose.position.y = dic_msg['data']['coordinates']['y']
            pose.pose.position.z = dic_msg['data']['coordinates']['z']
            pose.pose.orientation.x = -1 * dic_msg['data']['tagData']['eulerAngles']['z']
            pose.pose.orientation.y = -1 * dic_msg['data']['tagData']['eulerAngles']['y']
            pose.pose.orientation.z = 360 - dic_msg['data']['tagData']['eulerAngles']['x']
            # pose.pose.orientation.x = dic_msg['data']['tagData']['quaternion']['y']
            # pose.pose.orientation.y = dic_msg['data']['tagData']['quaternion']['z']
            # pose.pose.orientation.z = dic_msg['data']['tagData']['quaternion']['w']
            # pose.pose.orientation.w = dic_msg['data']['tagData']['quaternion']['x']
            # magnetic fields
            mag.magnetic_field.x = dic_msg['data']['tagData']['magnetic']['x']
            mag.magnetic_field.y = dic_msg['data']['tagData']['magnetic']['y']
            mag.magnetic_field.z = dic_msg['data']['tagData']['magnetic']['z']
            # imu data linear_acc, angular_vel, orientation
            imu.linear_acceleration.x = dic_msg['data']['tagData']['gravityVector']['x']
            imu.linear_acceleration.y = dic_msg['data']['tagData']['gravityVector']['y']
            imu.linear_acceleration.z = dic_msg['data']['tagData']['gravityVector']['z']
            imu.angular_velocity.x = dic_msg['data']['tagData']['gyro']['x'] * 0.017448352875489  # cvt dps to rps
            imu.angular_velocity.y = dic_msg['data']['tagData']['gyro']['y'] * 0.017448352875489  # cvt dps to rps
            imu.angular_velocity.z = dic_msg['data']['tagData']['gyro']['z'] * 0.017448352875489  # cvt dps to rps
            imu.orientation.x = dic_msg['data']['tagData']['quaternion']['y']
            imu.orientation.y = dic_msg['data']['tagData']['quaternion']['z']
            imu.orientation.z = dic_msg['data']['tagData']['quaternion']['w']
            imu.orientation.w = dic_msg['data']['tagData']['quaternion']['x']

            ## flags about appending data or not
            if(count == 0):
                poses.data.append(pose)
                mags.data.append(mag)
                imus.data.append(imu)
                id_checker.append(dic_msg['tagId'])
                count += 1

            if pose.header.frame_id in id_checker:
                # rospy.loginfo("[%s] same coord", dic_msg['tagId'])
                pass
            else:
                id_checker.append(pose.header.frame_id)
                poses.data.append(pose)
                mags.data.append(mag)
                imus.data.append(imu)
        else:
            rospy.logdebug("no coord outputs")

    signal.signal(signal.SIGINT, signal_handler)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")

def timer_callback(event):
    global count
    if len(poses.data) != 0:
        mqtt_pose_pub.publish(poses)
        mqtt_mag_pub.publish(mags)
        mqtt_imu_pub.publish(imus)
    count = 0
    id_checker.clear()
    poses.data.clear()
    mags.data.clear()
    imus.data.clear()


def main():

    rospy.init_node("mqtt_local_api_node", anonymous=True)
    rospy.loginfo("[mqtt2ros] Local API node initialized")
    rospy.Timer(rospy.Duration(0.01), timer_callback)

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
