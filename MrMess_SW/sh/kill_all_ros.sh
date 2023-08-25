#!/bin/sh
# rosrun  pixhawk_controller pixhawk_controller &
killall roslaunch &
killall master_sync &
killall master_discovery

echo "I am done"