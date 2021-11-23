#!/usr/bin/env python
#coding=utf-8
import rospy
import sys
from rospy.exceptions import ROSInterruptException
from sensor_msgs.msg import JointState

IIWA_JOINT_NAME=['iiwa_joint_1','iiwa_joint_2','iiwa_joint_3','iiwa_joint_4','iiwa_joint_5','iiwa_joint_6','iiwa_joint_7']

def pos_pub(pos):
    rospy.init_node("iiwa_joint_state_publisher")
    pub = rospy.Publisher("/joint_states",JointState,queue_size=10)
    rate=rospy.Rate(10)
    msg=JointState()
    msg.name=IIWA_JOINT_NAME
    msg.position=pos
    while not rospy.is_shutdown():
        msg.header.stamp=rospy.Time.now()
        pub.publish(msg)
        rate.sleep()
    pass

if __name__=='__main__':
    if len(sys.argv)<8:
        rospy.logerr('Invalid number of parameters\nusage: '
                     './ur_joint_pos_pub.py '
                     'angle1 angle2 angle3 angle4 angle5 angle6 angle7(Units:rad)')
        sys.exit(0)
    else:
        try:
            pos=[]
            for i in range(7):
                pos.append(float(sys.argv[i+1]))
            pos_pub(pos)
        except ROSInterruptException:
            pass