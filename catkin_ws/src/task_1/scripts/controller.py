#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
x=0
y=0
v_x=0.5
v_y=1
def pose_callback(pose :Pose):
    global x
    global y
    x=pose.x
    y=pose.y
if __name__ == '__main__':
    rospy.init_node("controller")
    pub=rospy.Publisher("/turtle1/cmd_vel", Twist,queue_size=10)
    sub=rospy.Subscriber("/turtle1/pose", Pose, callback=pose_callback)
    rate=rospy.Rate(100)
    while not rospy.is_shutdown():
        msg=Twist()
        msg.linear.x=v_x
        msg.linear.y=v_y
        if x >=7 and v_x > 0:
            v_x=-v_x
        if x <=3 and v_x < 0:
            v_x=-v_x
        if y <=3 and v_y < 0:
            v_y=-v_y
        if y >=7 and v_y>0:
            v_y=-v_y
        pub.publish(msg)
        rospy.loginfo(x)
        rospy.loginfo(y)
        rate.sleep()


