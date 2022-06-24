#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn



def spawn_turtle_service(x, y, theta, name):
    spawn_turtle = rospy.ServiceProxy("spawn", Spawn)
    response = spawn_turtle(x, y, theta, name)


count = 2
name = f"turtle{count}"


class turtle:
    
    def __init__(self, name, vel_x, vel_y, pos_x, pos_y):
        self.name = name
        self.x = pos_x
        self.y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        spawn_turtle_service(self.x, self.y,0, name)
    def pose_callback(self,pose: Pose):
        self.x = pose.x
        self.y = pose.y

    def controller(self):
        rate = rospy.Rate(100)
        msg = Twist()
        msg.linear.x = self.vel_x
        msg.linear.y = self.vel_y
        pub = rospy.Publisher(f"/{self.name}/cmd_vel", Twist, queue_size=10)
        sub = rospy.Subscriber(f"/{self.name}/pose", Pose, callback=self.pose_callback)
        if self.x >= 6.5 and self.vel_x > 0:
            self.vel_x = -self.vel_x
            count = count + 1
            turtle[count] = turtle(
                name,
                -turtle[count - 1].vel_x,
                [count - 1].vel_y,
                [count - 1].x,
                [count - 1].y,
            )
        if self.x <= 1 and self.vel_x < 0:
            self.vel_x = -self.vel_x
            count = count + 1
            turtle[count] = turtle(
                name,
                -[count - 1].vel_x,
                [count - 1].vel_y,
                [count - 1].x,
                [count - 1].y,
            )
        if self.y <= 1 and self.vel_y < 0:
            self.vel_y = -self.vel_y
            count = count + 1
            turtle[count] = turtle(
                name,
                [count - 1].vel_x,
                -[count - 1].vel_y,
                [count - 1].x,
                [count - 1].y,
            )
        if self.y >= 6.5 and self.vel_y > 0:
            self.vel_y = -self.vel_y
            count = count + 1
            turtle[count] = turtle(
                name,
                [count - 1].vel_x,
                -[count - 1].vel_y,
                [count - 1].x,
                [count - 1].y,
            )
        rospy.loginfo(self.x)
        rospy.loginfo(self.y)
        pub.publish(msg)
        rate.sleep()


if __name__ == "__main__":
    rospy.init_node("controller")
    rospy.wait_for_service("/spawn")
    turtle_obj = [0] * 17
    while not rospy.is_shutdown():
        rate = rospy.Rate(100)
        turtle_obj[count] = turtle(name, 1, 0.5, 5, 5)
        turtle_obj[count].controller()
        rate.sleep()
