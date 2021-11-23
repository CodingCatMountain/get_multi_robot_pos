#!/usr/bin/env python
#coding=utf-8
import ros
import rospy
import geometry_msgs.msg
from rospy.impl.tcpros_service import wait_for_service
import tf2_ros
# 请记住是功能.msg 导入自定义消息
from multi_robot.msg import baxter_joint_pos 

def listener():
    rospy.init_node("baxter_left_hand_pos_listener")

    # 实例化一个tf的listener
    tfBuffer = tf2_ros.Buffer()
    baxter_left_hand_listener = tf2_ros.TransformListener(tfBuffer)

    pub = rospy.Publisher("baxter_left_hand_pos",baxter_joint_pos,queue_size=10)
    rate=rospy.Rate(10.0)
    baxter_joint_names = ['left_upper_shoulder','left_lower_shoulder','left_upper_elbow','left_lower_elbow','left_upper_forearm','left_lower_forearm','left_wrist','left_hand','left_gripper_base','left_gripper_base']
    while not rospy.is_shutdown():
        try:
            trans=[]
            for i in range(len(baxter_joint_names)):
                trans.append(tfBuffer.lookup_transform(baxter_joint_names[i],'left_arm_mount',rospy.Time()))
        except (tf2_ros.LookupException,tf2_ros.ConnectivityException,tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        pos = []
        for i in range(len(baxter_joint_names)):
            pos.append(trans[i].transform.translation)
        
        # 自定义的消息类型
        msg = baxter_joint_pos()
        msg.child_frame_id=baxter_joint_names
        msg.translation=pos
        
        pub.publish(msg)

        rate.sleep()



if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass