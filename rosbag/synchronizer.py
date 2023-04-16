#!/usr/bin/env python

import rospy
import rosbag
from sensor_msgs.msg import Image, PointCloud2
from geometry_msgs.msg import TwistStamped
from message_filters import ApproximateTimeSynchronizer, Subscriber

# Callback function to receive and process synchronized messages
def callback(image_msg, point_msg):
    # print('Image timestamp: ', image_msg.header.stamp)
    # print('point timestamp: ', point_msg.header.stamp)
    time_diff = (image_msg.header.stamp - point_msg.header.stamp).to_sec()
    print('Time difference between messages:', time_diff, 'seconds')
    # if image_msg.header.stamp == point_msg.header.stamp:
        # print('Writing synchronized message to bag file')
    bag.write('/synced_image', image_msg, t=image_msg.header.stamp)
    bag.write('/synced_point_cloud', point_msg, t=point_msg.header.stamp)


# Initialize ROS node
rospy.init_node('message_sync')

# Set up rosbag recording
bag = rosbag.Bag('sync.bag', 'w')

# Set up message subscribers
image_sub = Subscriber('/usb_cam/image_raw', Image)
point_sub = Subscriber('/points_raw', PointCloud2)

# Set up approximate time synchronizer
ats = ApproximateTimeSynchronizer([image_sub, point_sub], queue_size=10, slop=0.1)
ats.registerCallback(callback)

# Start recording
# bag.start()

# Start processing incoming messages
rospy.spin()

# Stop recording
bag.close()
