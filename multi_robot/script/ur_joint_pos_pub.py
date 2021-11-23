#!/usr/bin/env python
#coding=utf-8
import rospy
import sys
from rospy.exceptions import ROSInterruptException
from sensor_msgs.msg import JointState

UR_JOINT_NAME=['ur5_shoulder_pan_joint','ur5_shoulder_lift_joint','ur5_elbow_joint','ur5_wrist_1_joint','ur5_wrist_2_joint','ur5_wrist_3_joint']

def pos_pub(pos):
    rospy.init_node("ur_joint_state_publisher")
    pub = rospy.Publisher("/joint_states",JointState,queue_size=10)
    rate=rospy.Rate(10)
    msg=JointState()
    msg.name=UR_JOINT_NAME
    msg.position=pos
    while not rospy.is_shutdown():
        msg.header.stamp=rospy.Time.now()
        pub.publish(msg)
        rate.sleep()
    pass

if __name__=='__main__':
    if len(sys.argv)<7:
        rospy.logerr('Invalid number of parameters\nusage: '
                     './ur_joint_pos_pub.py '
                     'angle1 angle2 angle3 angle4 angle5 angle6(Units:rad)')
        sys.exit(0)
    else:
        try:
            pos=[]
            for i in range(6):
                pos.append(float(sys.argv[i+1]))
            pos_pub(pos)
        except ROSInterruptException:
            pass