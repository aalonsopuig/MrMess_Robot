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
from math import radians
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
#GUI modules
import ttk
import Tkinter as tk
import tkFont

#constants
StopPoints_filename = '/home/turtlebot/catkin_ws/src/home_servant/data/home_data.csv'
logfilename='/home/turtlebot/catkin_ws/src/home_servant/data/_log.txt'
#StopPoints_filename = '/home/alejandro/catkin_ws/src/home_servant/data/home_data.csv'
#logfilename='/home/alejandro/catkin_ws/src/home_servant/data/_log.txt'

StopPoints = []   #List from file of StopPoints data
origin_wp = 0 					 #Item 0 in StopPoints[] refers to data of origin (charging point for AGV)
#index names from the content of StopPoints and origin_wp:
i_StopPoint_name = 0        		#This one is added in this program, as master index of this list
i_Position_X = 1			#Rack number
i_Position_Y = 2			#Aisle number
i_Orientation_Z = 3
i_Orientation_W = 4		#Sequence order


list_of_widgets = []		#Used to control the widgets created (tk/ttk)


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
	


  
def OutputLog(text, newline=True):
	#Print some log items
	if (newline):
		logfile.write(text)
		logfile.write("\r\n")
	else:
		logfile.write(text)
	return



## GUI FUNCTIONS AND CLASSES


def add_empty_rows(from_row_num, till_row_num):
#Create some empty rows for GUI
	for row_num in range(from_row_num, till_row_num+1):
		empty_space = ttk.Label(content, text=' ') 
		empty_space.grid(column=0, row=row_num)

def clearwidgets(list_of_widgets):
#Eliminate a list of Widgets from the GUI
    for widget in list_of_widgets:
        widget.destroy()



############################################################################
##     MAIN BODY
############################################################################

# INICIALIZATION PART ************************************************************************

#Some inicialization variables

#Start Log file
logfile=open(logfilename,'w') 
OutputLog('\r\nStarting System ')
OutputLog('Generating Log file ' + logfilename)
OutputLog('')

mr_mess_ctrl# we load Stop Points data
StopPoints_data_file=open(StopPoints_filename)

#Load StopPoints_data_file file. It contains the waypoints for AGV 
OutputLog('Importing Stop Points csv file')
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
helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)

#Load logo
#logo = tk.PhotoImage(file=logo_filename)
#label = tk.Label(content,image=logo, width=200, height=100)
#label.image = logo # keep a reference!
#label.grid(column=0, row=0, sticky=(tk.N, tk.W), columnspan=2)
label = ttk.Label(content, text='MISTER MESS') 
label.grid(column=0, row=1, sticky=(tk.W))
add_empty_rows(2, 3)
bt_quit=tk.Button(content, text='QUIT', font=helv36, height=1, width=15,command=root.quit)
list_of_widgets.append(bt_quit)
bt_quit.grid(column=2, row=4)


for StopPoint_num in range(0,len(StopPoints),2):
	bt_StopPoint=tk.Button(content, height=1, width=15, font=helv36, text=StopPoints[StopPoint_num][i_StopPoint_name], command=lambda StopPoint_num=StopPoint_num: goto_StopPoint(StopPoint_num))
	list_of_widgets.append(bt_StopPoint)
	bt_StopPoint.grid(column=1, row=5+StopPoint_num)

	if StopPoint_num < len(StopPoints)-1:
		bt_StopPoint=tk.Button(content, height=1, width=15, font=helv36, text=StopPoints[StopPoint_num+1][i_StopPoint_name], command=lambda StopPoint_num=StopPoint_num: goto_StopPoint(StopPoint_num+1))
		list_of_widgets.append(bt_StopPoint)
		bt_StopPoint.grid(column=2, row=5+StopPoint_num)



# MAIN ROS PART ************************************************************************

#We continue with ROS modules
rospy.init_node('mr_mess_ctrl_node')
#		sub=rospy.Subscriber('/scan', LaserScan, scan_callback)
#		cmd_vel_ = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)
rate = rospy.Rate(20)
#		move_cmd = Twist()		# Twist is a datatype for velocity

rospy.sleep(1)			# delay to ensure everything starts stable
#	Ti = rospy.Time.now()					# initial time, for set_twist() function

movebase_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
print 'waiting for server...'
movebase_client.wait_for_server()
print 'server ready'

#while not rospy.is_shutdown():		# Create a loop that will go until someone stops the program execution



rospy.sleep(1)

#	rate.sleep()

root.mainloop() #The window won't appear until we enter the Tkinter event loop
root.destroy()
OutputLog('End of program. Closing log file')
logfile.close()

