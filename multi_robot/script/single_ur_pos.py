#!/usr/bin/env python
import ros
import rospy
import geometry_msgs.msg
from rospy.impl.tcpros_service import wait_for_service
import tf2_ros
# 请记住是功能.msg 导入自定义消息
from multi_robot.msg import ur5_joint_pos 

def listener():
    rospy.init_node("single_ur5_pos_listener")

    # 实例化一个tf的listener
    tfBuffer = tf2_ros.Buffer()
    ur5_listener = tf2_ros.TransformListener(tfBuffer)

    pub = rospy.Publisher("single_ur5_pos",ur5_joint_pos,queue_size=10)
    rate=rospy.Rate(10.0)
    ur5_joint_names = ['shoulder_link','upper_arm_link','forearm_link','wrist_1_link','wrist_2_link','wrist_3_link']
    while not rospy.is_shutdown():
        try:
            trans=[]
            for i in range(len(ur5_joint_names)):
                trans.append(tfBuffer.lookup_transform(ur5_joint_names[i],'base',rospy.Time()))
        except (tf2_ros.LookupException,tf2_ros.ConnectivityException,tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        pos = []
        for i in range(len(ur5_joint_names)):
            pos.append(trans[i].transform.translation)
        
        # 自定义的消息类型
        msg = ur5_joint_pos()
        msg.child_frame_id=ur5_joint_names
        msg.translation=pos
        
        pub.publish(msg)

        rate.sleep()



if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass