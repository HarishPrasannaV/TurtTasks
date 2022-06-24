#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn, Kill

count = 1
name = None
turt = [0] * 20

class turtle:
    global count
    global name
    x = None
    y = None
    v_x = None
    v_y = None
    name = f"turtle{count}"

    def callback(self, pose):
        self.x = pose.x
        self.y = pose.y

    def __init__(self, name, x, y, v_x, v_y):
        self.name = name
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.spawn_turtle = rospy.ServiceProxy("/spawn", Spawn)
        self.response = self.spawn_turtle(self.x, self.y, 0, self.name)
        self.pub = rospy.Publisher(f"/{self.name}/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber(f"/{self.name}/pose", Pose, callback=self.callback)

    def controller(self):
        global count
        global name
        self.msg = Twist()
        u=self.msg.linear.x = self.v_x
        v=self.msg.linear.y = self.v_y
        if self.x >= 9 and self.v_x > 0:
            self.v_x = -self.v_x
            
            ln = f"name{count}"
            if count<16:
                count = count + 1
                turt[count] = turtle(ln, self.x, self.y, -u, -v)
                turt[count].controller()
        if self.x <= 2 and self.v_x < 0:
            self.v_x = -self.v_x
            
            ln = f"name{count}"
            if count<16:
                count = count + 1
                turt[count] = turtle(ln, self.x, self.y, -u, -v)
                turt[count].controller()

        if self.y >= 9 and self.v_y > 0:
            self.v_y = -self.v_y
            
            ln = f"name{count}"
            if count<16:
                count = count + 1
                turt[count] = turtle(ln, self.x, self.y, -u, -v)
                turt[count].controller()

        if self.y <= 2 and self.v_y < 0:
            self.v_y = -self.v_y
            
            ln = f"name{count}"
            if count<16:
                count = count + 1
                turt[count] = turtle(ln, self.x, self.y, -u, -v)
                turt[count].controller()
        
        self.pub.publish(self.msg)



if __name__ == "__main__":
    rospy.init_node("node")
    rospy.wait_for_service("/kill")
    rospy.wait_for_service("/spawn")
    kill_turtle = rospy.ServiceProxy("/kill", Kill)
    response = kill_turtle("turtle1")
    turt[count] = turtle(name, 5, 5, 2, 0.5)
  
    while not rospy.is_shutdown():
        turt[count].controller()
        for i in range(1,count):
            turt[i].controller()
            
        
    
    
