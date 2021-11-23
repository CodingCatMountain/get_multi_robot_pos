#!/usr/bin/env python
#coding=utf-8
import rospy
import sys
from rospy.exceptions import ROSInterruptException
from sensor_msgs.msg import JointState

BAXTER_LEFT_JOINT_NAME=['left_s0','left_s1','left_e0','left_e1','left_w0','left_w1','left_w2']

def pos_pub(pos):
    rospy.init_node("baxter_left_joint_state_publisher")
    pub = rospy.Publisher("/joint_states",JointState,queue_size=10)
    rate=rospy.Rate(10)
    msg=JointState()
    msg.name=BAXTER_LEFT_JOINT_NAME
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