#!/usr/bin/env python
import ros
import rospy
from rospy.exceptions import ROSInternalException, ROSInterruptException
import tf
from tf2_msgs.msg import TFMessage
import tf2_msgs
import tf2_ros
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node("single_ur5_pos_listener")

    tfBuffer =tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    
    pub = rospy.Publisher("single_ur5_pos",geometry_msgs.msg.TransformStamped,queue_size=10)
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            trans=tfBuffer.lookup_transform('ee_link','base',rospy.Time())
        except (tf2_ros.LookupException,tf2_ros.ConnectivityException,tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
        
        msg = geometry_msgs.msg.TransformStamped()
        msg.child_frame_id = "ee_link"
        msg.transform.translation=trans.transform.translation

        pub.publish(msg)

        rate.sleep()

        

