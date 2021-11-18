cmake_minimum_required(VERSION 3.0.2)
project(mqtt2ros)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  geometry_msgs
  sensor_msgs
  rospy
  std_msgs
)

add_message_files(
  FILES
  mqtt_msg.msg
  mqtt_mag.msg
  mqtt_imu.msg
)

generate_messages(
  DEPENDENCIES
  geometry_msgs
  sensor_msgs
)

catkin_package(
  CATKIN_DEPENDS geometry_msgs sensor_msgs rospy std_msgs message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

