# MrMess_Robot
**SLAM based robot able to navigate to different parts of a building**

Abril 2018 <BR>
Proyect made by Alejandro Alonso Puig

---
The purpose of this project is to configure and program a robot in Python with ROS1 to go autonomously to specific locations on demand. A touch screen will show the locations. The user could put some weight on the robot and push the touchscreen for another destination to deliver the goods. This might be useful for home or office.

![image](https://github.com/aalonsopuig/MrMess_Robot/assets/57196844/bd31c099-314e-4334-b824-f7f429291fae)

You could see a video of the robot in action here: https://youtu.be/iOwSirOZlpU?si=c7tDH9yB6HjSfDAF

In this repository you will find the documentation of the project as well as the software.

I used a Turtlebot 2 robot with Kobuki base as robot platform, an RPLidar-1 as Lidar, a RaspberryPi-3B as embedded computer, a 7” touchscreen and a DCDC regulator 12v to 5v for powering the RaspberryPi and Lidar from the robot batteries.

![MrMess_HW_architecture](https://github.com/aalonsopuig/MrMess_Robot/assets/57196844/31efdbf4-ef7a-418a-9f61-65876bfde2ed)

The system uses ROS Kinetic over Ubuntu Mate Linux distribution on a Raspberry Pi 3B. See Annex 1 at the end of this document for instructions on how to install Ubuntu Mate, ROS Kinetic, Turtlebot/Kobuki ROS drivers and RPLidar ROS drivers.

Here is the Flowchart of the application developed. All is under a package called mr_mess and is executed from the launch file mr_mess.launch by using the command roslaunch mr_mess mr_mess.launch

![MrMess_SW_architecture](https://github.com/aalonsopuig/MrMess_Robot/assets/57196844/1006ed1e-a0b5-4703-a926-2e7a51f0b229)
