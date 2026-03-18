# Source - https://stackoverflow.com/a/24851547
# Posted by furas, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-18, License - CC BY-SA 4.0

from tkinter import *
import datetime

root = Tk()

lab = Label(root)
lab.pack()

def clock():
    time = datetime.datetime.now().strftime("Time: %H:%M:%S")
    lab.config(text=time)
    #lab['text'] = time
    root.after(1000, clock) # run itself again after 1000 ms
    
# run first time
clock()

root.mainloop()
