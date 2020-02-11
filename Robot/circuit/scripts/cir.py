#!/usr/bin/env python

import roslib
import rospy
import actionlib
from std_msgs.msg import String
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

interrupt_pys = False
interrupt_zig = False

#On définit notre publisher et on crée les 2 fonctions de callback à appeller quand on recevera un message sur les topics abonnés
pub = rospy.Publisher('arrive', String, queue_size=10)
 
def callback_pys(data):
    rospy.loginfo(rospy.get_caller_id() + "Pysense : %s", data.data)
    global interrupt_pys 
    interrupt_pys = True
 
def callback_zig(data):
    rospy.loginfo(rospy.get_caller_id() + "Zigduino : %s", data.data)
    global interrupt_zig 
    interrupt_zig = True
       

class NavTest():
    
    def __init__(self):
        global interrupt_pys
        global interrupt_zig
        global pub

        rospy.init_node('nav_test', anonymous=True)
        
        rospy.on_shutdown(self.shutdown)
        
        # Temps de pause à chaque étape
        self.rest_time = rospy.get_param("~rest_time", 5)
        
        # Vérifie si on est dans une simulation
        self.fake_test = rospy.get_param("~fake_test", False)
        
        # Les différents états des objectifs
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED', 
                       'SUCCEEDED', 'ABORTED', 'REJECTED',
                       'PREEMPTING', 'RECALLING', 'RECALLED',
                       'LOST']
        

        # Liste des localisations que le robot tentera de rejoindre
        locations = []
        
        locations.append( Pose(Point(-2.2, 9, 0.000), Quaternion(0.000, 0.000, 0.223, 0.975)))
        locations.append( Pose(Point(-3.7, 7.21, 0.000), Quaternion(0.000, 0.000, -0.670, 0.743)))
        locations.append( Pose(Point(3.8, 1.75, 0.000), Quaternion(0.000, 0.000, 0.733, 0.680)))

        # Publisher pour controler le robot manuellement
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        
        # Subscribe au serveur move_base action 
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
        rospy.loginfo("Waiting for move_base action server...")
        self.move_base.wait_for_server(rospy.Duration(60))
        rospy.loginfo("Connected to move base server")
        
        # Position de départ
        initial_pose = PoseWithCovarianceStamped()
        
        # Variables
        n_locations = len(locations)
        i = 0
        location = ""
        
        # Demande de la position de départ sur rviz
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)
        
        # Vérifie que l'on a bien une position de départ
        while initial_pose.header.stamp == "":
            rospy.sleep(1)
            
        rospy.loginfo("Starting navigation test")
        
        # Loop principal
        while not rospy.is_shutdown():
            i += 1
            if i == n_locations:
                i = 0
                        
            
            # Configuration du prochain objectif
            self.goal = MoveBaseGoal()
            self.goal.target_pose.pose = locations[i]
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            
            # Affiche le prochain objectif
            rospy.loginfo("Going to pos " + str(i))
            
            # Démarre le déplacement du robot
            self.move_base.send_goal(self.goal)
            


            while not self.move_base.wait_for_result(rospy.Duration(1)):
                
                if interrupt_zig : 
                    self.move_base.cancel_goal()
                    rospy.sleep(2)
                    self.goal = MoveBaseGoal()
                    # Destination 
                    self.goal.target_pose.pose = locations[1]
                    self.goal.target_pose.header.frame_id = 'map'
                    self.goal.target_pose.header.stamp = rospy.Time.now()
                    
                    # Oon rentre a la base
                    rospy.loginfo("ALERTE ZIGDUINO")
                    rospy.loginfo("Going to pos 1")

                    self.move_base.send_goal(self.goal)
                    interrupt_zig = False

                if interrupt_pys : 
                    self.move_base.cancel_goal()
                    rospy.sleep(2)
                    self.goal = MoveBaseGoal()
                    # Destination 
                    self.goal.target_pose.pose = locations[2]
                    self.goal.target_pose.header.frame_id = 'map'
                    self.goal.target_pose.header.stamp = rospy.Time.now()
                    
                    # On rentre a la base
                    rospy.loginfo("ALERTE Pysense")
                    rospy.loginfo("Going to pos 2")

                    self.move_base.send_goal(self.goal)
                    interrupt_pys = False                    

        
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("Goal succeeded!")
                rospy.loginfo("State:" + str(state))
            else:
                rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))
            
            # Fin de l'etape -> envoi un message au topic 
            message = "fin etape"
            rospy.loginfo(message)
            pub.publish(message)

            rospy.sleep(self.rest_time)
            
    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.move_base.cancel_goal()
        rospy.sleep(2)
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)
      
def trunc(f, n):
    # Truncates/pads a float f to n decimal places without rounding
    slen = len('%.*f' % (n, f))
    return float(str(f)[:slen])

if __name__ == '__main__':
    try:
        rospy.Subscriber("zigduino", String, callback_zig)
        rospy.Subscriber("pysense", String, callback_pys)
        
        NavTest()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AMCL navigation test finished.")
