'''

Project: BreezyUI Version b1.0.1 (b1.0.1.py)
Author: JonoCode9374
Date Created: 3/8/2018
Description:

Many Python users who work with graphical interfaces know the pains of
designing and creating a Graphical User Interface with Python’s built-in
graphics library tkinter (Tkinter in Python 2 and tkinter in Python 3) –
creating interfaces requires intense planning (getting the co-ordinates
for where each widget goes), lots of trial and error. This is what I
have personally experienced many times, making programs such as my SpamBot,
DocEdit and my Head Scruiteneer Program.

'''

import tkinter
from tkinter import dnd #Accessed with `tkinter.dnd`. Provides drag'n'drop
                        #services                                        .
import functools
import screens
import tkinter.colorchooser as tkColor

class DndWidget():
    
    def __init__(self, widget, **kwargs):
        '''
        Takes:
        - self
        - widget [str] -- The type of widget that this instance will be
        - kwargs [dict] -- Arguments used to build widget later on

        Does:
        - Initalises the instance of DndWidget

        Returns:
        - None
        '''
        self.widget_type = widget
        self.canvas = self.widget = self._id = None
        self.kwargs = kwargs

    def attach(self, canvas, x=10, y=10):
        '''
        Takes:
        - self
        - canvas [tkinter.Canvas()] -- The canvas the widget will be attached to
        - x [int] -- The x position of the widget (def. 10)
        - y [int] -- The y position of the widget (def. 10)

        Does:
        - Attaches the widget to the given canvas at the provided co-ordinates
        - Creates the widget
        - Binds it to functions allowing it to function

        Returns:
        - None
        '''

        global target_widget

        if canvas is self.canvas:
            self.canvas.coords(self._id, x, y)
            return

        if self.canvas:
            self.detach()

        if not canvas:
            return

        widget = eval("tkinter.{0}(canvas, {1})".format(self.widget_type, ', '\
                                                        .join([str(x) + '=' +\
                                                        self\
                                                        .kwargs[x] for x in self\
                                                        .kwargs])))

        #The above list comprehension reads as so:
        #`", ".join([str(x) + "=" + self.args[x] for x in self.args])

        _id = canvas.create_window(x, y, window=widget, anchor="nw")
        self.canvas = canvas
        self.widget = widget
        self._id = _id
        self.x_off = 0
        self.y_off = 0
        widget.bind("<ButtonPress>", self.press)
        self.widget.bind("<Button-2>", functools.partial(edit_attributes,
                                                         source=self.widget))

    def detach(self):
        '''
        Takes:
        - self

        Does:
        - Detaches the widget from the canvas
        - Destroys the widget

        Returns:
        - None
        '''

        canvas = self.canvas
        if not canvas: return

        _id = self._id
        widget = self.widget
        self.canvas = self.widget = self._id = None
        canvas.delete(_id)
        widget.destroy

    def press(self, event):
        '''
        Takes:
        - self
        - event [?] -- the event that happened when the widget was clicked?

        Does:
        - ?

        Returns:
        - None
        '''

        if tkinter.dnd.dnd_start(self, event):
            # where the pointer is relative to the widget widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self._id)

    def move(self, event):
        '''
        Takes:
        - self
        - event [?] -- don't know what it is for

        Does:
        - Moves the widget on the canvas
        - Updates the internal co-ordinates

        Returns:
        - None
        '''

        x, y = self.where(self.canvas, event)
        self.canvas.coords(self._id, x, y)

    def putback(self):
        '''
        Takes:
        - self

        Does:
        - I'm not too sure

        Returns:
        - None
        '''

        self.canvas.coords(self._id, self.x_orig, self.y_orig)

    def where(self, canvas, event):
        '''
        Takes:
        - self
        - canvas [tkinter.Canvas()] -- The canvas which the widget is on
        - event [?] -- ?

        Does:
        - Calculates the relative position of the widget

        Returns:
        - (int) -- A tuple with the relative position of the widget
        '''

        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x - self.x_off, y - self.y_off

    def dnd_end(self, target, event):
        '''
        Stub function? I'm not sure. Not much need to document this,
        as it only does nothing. I think that this function is needed
        for compatability with the tkinter.dnd library
        '''

        pass

class DndSpace:
    def __init__(self, root, width, height):
        '''
        Takes:
        - self
        - root [tkinter.Tk()] -- the window which the space will be on
        - width [int] -- the width of the canvas
        - height [int] -- the height of the canvas

        Does:
        - Intalises this instance of DndSpace

        Returns:
        - None
        '''

        self.top = tkinter.Toplevel(root)
        self.canvas = tkinter.Canvas(self.top, width=width, height=height)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.dnd_accept = self.dnd_accept


    #The next function is more of a compability function, I believe, as it just
    #returns self                                                             .

    def dnd_accept(self, source, event):
        '''
        For reasons explained above, there will be no documentation for this
        function
        '''

        return self

    def dnd_enter(self, source, event):
        '''
        Takes:
        - self
        - source [tkinter widget] -- the widget being moved onto the DndSpace
        - event [?] -- ?

        Does:
        - Sets up the widget for when it is dragged onto the DndSpace

        Returns:
        - None
        '''

        self.canvas.focus_set() # Show highlight border
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = source.canvas.bbox(source._id)
        dx, dy = x2-x1, y2-y1
        self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
        self.dnd_motion(source, event)

    #I won't comment the next few fuxnctions, as I don't quite understand them in
    #enough detail to provide what they take, do and return                    .
        
    def dnd_motion(self, source, event):
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
        self.canvas.move(self.dndid, x-x1, y-y1)

    def dnd_leave(self, source, event):
        self.top.focus_set() # Hide highlight border
        self.canvas.delete(self.dndid)
        self.dndid = None

    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = source.where(self.canvas, event)
        source.attach(self.canvas, x, y)

class CoreWidget:

    row = column = 0
    
    def __init__(self, widget_type, **kwargs):
        '''
        Takes:
        - self
        - widget_type -- The type of tkinter widget that the instance will be
        '''

        self.widget_type = widget_type
        self.widget = eval("tkinter.{0}(attributes_area, {1})".format\
                           (widget_type, kwargs))

        self.widget.grid(row=row, column=column)

        if column == 1:
            row += 1
            column = 0
        else:
            column = 1

        widget.bind("<ButtonPress>", functools.partial(on_dnd_start, widget_type=\
                                                         widget_type))
        


def on_dnd_start(event, widget_type):
    '''
    This is invoked when a widget is dragged onto the main canvas.
    '''

    #Create the widget to be dragged
    dnd_widget = DndWidget(widget_type, text='"Text"') #Maybe soon,
                                                       #make this dynamic
    dnd_widget.attach(widget_area.canvas)
    tkinter.dnd.dnd_start(dnd_widget, event)

def edit_attributes(event, source):
    global target_widget
    target_widget = source

    #Show the changable attributes of the target widget
    for item in options:
        options[item][0].grid(row=options[item][1][0],
                              column=options[item][1][1])

    #options["text.entry"]

def hide_attributes():
    for item in options:
        options[item][0].grid_forget()
    options["text.entry"][0].delete("0", tkinter.END)

def update_widget():
    target_widget.config({"text" : options["text.entry"][0].get()})
    target_widget.config({"bg" : colour})
    hide_attributes()

def choose_colour():
    global colour
    colour = tkColor.askcolor()[1]
    options["bg.picker"][0]


target_widget = None

root = tkinter.Tk()
root.withdraw() #The root window wont be used in this program

main_area = DndSpace(root, 800, 600)
main_area.top.geometry("+1+60")

widget_area = DndSpace(root, 200, 600)
widget_area.top.geometry("+803+60")



widgets = dict() #A dictionary to store all the widget objects which the clones will
                 #come from

widgets["label"] = CoreWidget("Label", text="Label")
widgets["button"] = CoreWidget("Button", text="Button")
widgets["entry"] = CoreWidget("Entry", textvariable=tkinter\
                              .StringVar(root, value="Entry"))
                                                    


widgets["button"] = tkinter.Button(widget_area.canvas, text="Button")
widgets["button"].pack()
widgets["button"].bind("<ButtonPress>", functools.partial(on_dnd_start,
                                                        widget_type=\
                                                         "Button"))

widgets["entry"] = tkinter.Entry(widget_area.canvas, textvariable=tkinter.\
                                 StringVar\
                                 (root, value="Entry"))
widgets["entry"].pack()
widgets["entry"].bind("<ButtonPress>", functools.partial(on_dnd_start,
                                                         widget_type=\
                                                         "Entry"))

attributes_area = tkinter.Tk()
attributes_area.geometry("+803+160")


options = dict() #A dictionary to store all the attributes shown in the
                 #attributes area

options["text.label"] = [tkinter.Label(attributes_area, text="Display Text"),
                         (0, 0)]
options["text.entry"] = [tkinter.Entry(attributes_area), (0, 1)]


options["bg.label"] = [tkinter.Label(attributes_area, text="Background Colour"),
                       (1, 0)]
options["bg.picker"] = [tkinter.Button(attributes_area, text="  ",
                                      command=choose_colour), (1, 1)]

options["confirm"] = [tkinter.Button(attributes_area,
                                    text="Confirm", command=update_widget),
                      (2, 1)]

colour = "#ffffff"
    
        
        
'''≈≈'''

        
