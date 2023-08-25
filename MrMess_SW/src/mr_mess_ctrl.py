#! /usr/bin/env python
""" Package: MISTER MESS
    Author: Alejandro Alonso 
	Date: April 2018
    Purpose: makes the turtlebot go to certain points in a map 

"""
import csv #for importing data from CSV files
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

#GUI modules
import ttk
import Tkinter as tk
import tkFont

#constants
StopPoints_filename = '/home/turtlebot/catkin_ws/src/mr_mess/data/stop_points.csv'
#StopPoints_filename = '/home/alejandro/catkin_ws/src/mr_mess/data/stop_points.csv'

StopPoints = []   #List from file of StopPoints data
origin_wp = 0 	#Item 0 in StopPoints[] refers to data of origin (charging point for AGV)
#index names from the content of StopPoints and origin_wp:
i_StopPoint_name = 0        		#This one is added in this program, as master index of this list
i_Position_X = 1			#Rack number
i_Position_Y = 2			#Aisle number
i_Orientation_Z = 3
i_Orientation_W = 4		#Sequence order


def goal_pose(pose):
	#A helper function to turn a waypoint into a MoveBaseGoal
	goal_pose = MoveBaseGoal()
	goal_pose.target_pose.header.frame_id = 'map'
	goal_pose.target_pose.pose.position.x = float(pose[0][0])
	goal_pose.target_pose.pose.position.y = float(pose[0][1])
	goal_pose.target_pose.pose.position.z = float(pose[0][2])
	goal_pose.target_pose.pose.orientation.x = float(pose[1][0])
	goal_pose.target_pose.pose.orientation.y = float(pose[1][1])
	goal_pose.target_pose.pose.orientation.z = float(pose[1][2])
	goal_pose.target_pose.pose.orientation.w = float(pose[1][3])
	return goal_pose


def goto_StopPoint(StopPoint_num):
#Send agv no selected stop point
	
	print 'AGV moves to Stop Point', StopPoint_num
	Position_X = StopPoints[StopPoint_num][i_Position_X]
	Position_Y = StopPoints[StopPoint_num][i_Position_Y]
	Position_Z = 0
	Orientation_X = 0
	Orientation_Y = 0
	Orientation_Z = StopPoints[StopPoint_num][i_Orientation_Z]
	Orientation_W = StopPoints[StopPoint_num][i_Orientation_W]
	next_StopPoint = [(Position_X, Position_Y, Position_Z), (Orientation_X, Orientation_Y, Orientation_Z, Orientation_W)]
	goal = goal_pose(next_StopPoint)
	movebase_client.send_goal(goal)
	movebase_client.wait_for_result()
	




############################################################################
##     MAIN BODY
############################################################################

# INICIALIZATION PART ************************************************************************

# we load Stop Points data
StopPoints_data_file=open(StopPoints_filename)
for row in csv.reader(StopPoints_data_file):  #Read each row of file as list
	StopPoints.append(row)           #append to the data list the row read (lists) 
StopPoints_data_file.close()    
StopPoints.pop(0)			#We remove the first item as it includes only titles


# GUI GENERATION PART ************************************************************************

root = tk.Tk()

# Add a grid
content = ttk.Frame(root)
content.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), pady=10, padx=10)

#Font definition
#helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
helv26 = tkFont.Font(family='Helvetica', size=26, weight=tkFont.BOLD)

label = tk.Label(content, text=' Mister Mess Robot ', font=helv26, fg="blue") 
label.grid(column=0, row=1, columnspan=2)

#We create the buttons for the StopPoints
for StopPoint_num in range(0,len(StopPoints),2):
	bt_StopPoint=tk.Button(content, height=1, width=19, font=helv26, text=StopPoints[StopPoint_num][i_StopPoint_name], command=lambda StopPoint_num=StopPoint_num: goto_StopPoint(StopPoint_num))
	bt_StopPoint.grid(column=0, row=2+StopPoint_num)

	if StopPoint_num < len(StopPoints)-1:
		bt_StopPoint=tk.Button(content, height=1, width=19, font=helv26, text=StopPoints[StopPoint_num+1][i_StopPoint_name], command=lambda StopPoint_num=StopPoint_num: goto_StopPoint(StopPoint_num+1))
		bt_StopPoint.grid(column=1, row=2+StopPoint_num)

bt_quit=tk.Button(content, text='Quit', font=helv26, fg="red", height=1, width=8,command=root.quit)
bt_quit.grid(column=1, row=3+StopPoint_num, sticky=(tk.E))


# ROS PART ************************************************************************

#We continue with ROS modules
rospy.init_node('mr_mess_ctrl_node')
rate = rospy.Rate(20)
rospy.sleep(1)			# delay to ensure everything starts stable
movebase_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
print 'waiting for server...'
movebase_client.wait_for_server()
print 'server ready'

root.mainloop() #The window won't appear until we enter the Tkinter event loop
root.destroy()

