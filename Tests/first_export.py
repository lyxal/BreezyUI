
#############################################################
#The following code was pre-generated by BreezyUI           #
#Don't change any of the code if you don't know what it does#
#############################################################

import sys
if sys.version_info[0] == 2:
    import Tkinter as tkinter #backwards compatability
else:
    import tkinter

root = tkinter.Tk()
root.geometry("800x600") #Set the size of the window

object0 = tkinter.Label(root, {'background': '#ffffff', 'bg': '#ffffff', 'text': 'Fiddle Diddle'})
object0.place(x=325,y=32)
object1 = tkinter.Entry(root, {})
object1.place(x=580,y=176)
object2 = tkinter.Button(root, {'text': 'Fiddle Riddle Diddle Diddle'})
object2.place(x=66,y=282)
object3 = tkinter.Label(root, {'background': '#1e00fe', 'bg': '#1e00fe', 'text': '#made_with_bUI'})
object3.place(x=337,y=498)
