#!/usr/bin/python3
import paho.mqtt.client as mqtt
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import MagneticField, Imu
from mqtt2ros.msg import mqtt_msg, mqtt_mag, mqtt_imu
import rospy
import ssl
import signal, sys

host = "mqtt.cloud.pozyxlabs.com"
port = 443
topic = "5f928c413528d3055d3093e5"
username = "5f928c413528d3055d3093e5"
password = "920a09b0-c5c6-4210-9e4c-60a0d0dff352"

ERROR = 54321
true = "True"
false = "False"    
count = 0

mqtt_pose_pub = rospy.Publisher('mqtt_coord', mqtt_msg, queue_size= 1)
mqtt_mag_pub  = rospy.Publisher('mqtt_mag', mqtt_mag, queue_size= 1)
mqtt_imu_pub  = rospy.Publisher('mqtt_imu', mqtt_imu, queue_size=1)

def signal_handler(sig, frame):
    print('Keyboard Ctrl+C! interrupted')
    sys.exit(0)

def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))

def on_message(client, userdata, msg):

    poses = mqtt_msg()
    mags = mqtt_mag()
    imus = mqtt_imu()

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

            mags.data.append(mag)
            poses.data.append(pose)
            imus.data.append(imu)
        else:
            print("no coordinate ouputs")
            # pose.pose.position.x = pose.pose.position.y = pose.pose.position.z = ERROR
        
    if(len(poses.data)!=0 and len(mags.data)!=0):
        poses.header.stamp = imus.header.stamp = mags.header.stamp = rospy.get_rostime()
        mqtt_pose_pub.publish(poses)
        mqtt_mag_pub.publish(mags)
        mqtt_imu_pub.publish(imus)

    signal.signal(signal.SIGINT, signal_handler)

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
