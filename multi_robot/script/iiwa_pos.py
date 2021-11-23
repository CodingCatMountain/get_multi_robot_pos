#!/usr/bin/env python
#coding=utf-8
import ros
import rospy
import geometry_msgs.msg
from rospy.impl.tcpros_service import wait_for_service
import tf2_ros
# 请记住是功能.msg 导入自定义消息
from multi_robot.msg import iiwa_joint_pos 

def listener():
    rospy.init_node("iiwa_pos_listener")

    # 实例化一个tf的listener
    tfBuffer = tf2_ros.Buffer()
    ur5_listener = tf2_ros.TransformListener(tfBuffer)

    pub = rospy.Publisher("iiwa_pos",iiwa_joint_pos,queue_size=10)
    rate=rospy.Rate(10.0)
    iiwa_joint_names = ['iiwa_link_1','iiwa_link_2','iiwa_link_3','iiwa_link_4','iiwa_link_5','iiwa_link_6','iiwa_link_7']
    while not rospy.is_shutdown():
        try:
            trans=[]
            for i in range(len(iiwa_joint_names)):
                trans.append(tfBuffer.lookup_transform(iiwa_joint_names[i],'iiwa_link_7',rospy.Time()))
        except (tf2_ros.LookupException,tf2_ros.ConnectivityException,tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        pos = []
        for i in range(len(iiwa_joint_names)):
            pos.append(trans[i].transform.translation)
        
        # 自定义的消息类型
        msg = iiwa_joint_pos()
        msg.child_frame_id=iiwa_joint_names
        msg.translation=pos
        
        pub.publish(msg)

        rate.sleep()



if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass