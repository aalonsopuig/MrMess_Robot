#! /usr/bin/env python

#GUI modules
import ttk
import Tkinter as tk
import rospy


def goto_StopPoint(StopPoint_num):
#Send agv no selected stop point
	
	print 'AGV moves to Stop Point', StopPoint_num



# GUI GENERATION PART ************************************************************************

root = tk.Tk()
# Add a grid
content = ttk.Frame(root)
content.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), pady=10, padx=10)


#Load logo
#logo = tk.PhotoImage(file=logo_filename)
#label = tk.Label(content,image=logo, width=200, height=100)
#label.image = logo # keep a reference!
#label.grid(column=0, row=0, sticky=(tk.N, tk.W), columnspan=2)
label = ttk.Label(content, text='HOME SERVANT') 
label.grid(column=0, row=1, sticky=(tk.W))
add_empty_rows(2, 3)


bt_StopPoint=tk.Button(content, height=5, width=15, text='tal', command=lambda: goto_StopPoint(3))
bt_StopPoint.grid(column=1, row=4)



bt_quit=tk.Button(content, text='Quit', command=root.quit)
bt_quit.grid(column=2, row=30)

rospy.init_node('nav_node')
rate = rospy.Rate(20)
rospy.sleep(1)

while not rospy.is_shutdown():
    print 'tal'

root.mainloop() #The window won't appear until we enter the Tkinter event loop
print 'cual'
root.destroy()
