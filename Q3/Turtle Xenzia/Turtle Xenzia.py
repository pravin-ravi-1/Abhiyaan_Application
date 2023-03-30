#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Kill, Spawn
from math import pow, atan2, sqrt
import random

kill_turtle = rospy.ServiceProxy('/kill', Kill)
spawn_turtle = rospy.ServiceProxy('/spawn', Spawn)
spawned = False
alive = True

class Hisoka:
    def __init__(self):
        rospy.init_node('turtle_xenzia', anonymous=True)

        rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)

        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

        self.pose = Pose()

        self.alive = True

    def update_pose(self, data):
        self.pose = data

    def distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move_turtle(self, goal_pose, distance_tolerance):
        vel_msg = Twist()

        # If Hisoka moves outside square region x=1,x=8,y=1,y=8
        if self.pose.x<1 or self.pose.x>8 or self.pose.y<1 or self.pose.y>8:
            kill_turtle('turtle1')
            self.alive = False

        # Loop until turtle reaches goal pose
        while self.distance(goal_pose) >= distance_tolerance and self.alive:
            # Set linear velocity of turtle
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Set angular velocity of turtle
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            self.velocity_publisher.publish(vel_msg)

        # Stop turtle when goal pose is reached
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    while alive:
        try:
            hisoka = Hisoka()

            if spawned:
                kill_turtle('prey')
            else:
                spawned = True

            goal_pose = Pose()
            goal_pose.x = random.randint(1, 8)
            goal_pose.y = random.randint(1, 8)
            goal_pose.theta = random.randint(0,360)

            spawn_turtle(x=goal_pose.x, y=goal_pose.y, theta=0, name='prey')

            distance_tolerance = 0.1

            hisoka.move_turtle(goal_pose, distance_tolerance)

        except rospy.ROSInterruptException:
            pass
