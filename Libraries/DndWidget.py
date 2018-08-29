import tkinter, functools
import bUI

edit_attributes = None

class DndWidget():
    id_number = 0
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
        self.canvas = self.widget = self._id =  None
        self.kwargs = kwargs
        self.name = "object{}".format(DndWidget.id_number)
        DndWidget.id_number += 1


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

        widget = eval("tkinter.{0}(canvas, {1})".format(self.widget_type, ', '.join([str(x) + '=' + self.kwargs[x] for x in self.kwargs])))



        _id = canvas.create_window(x, y, window=widget, anchor="nw")
        self.canvas = canvas
        self.widget = widget
        self._id = _id
        self.x_off = 0
        self.y_off = 0
        widget.bind("<ButtonPress>", self.press)
        self.widget.bind("<Button-2>", functools.partial(edit_attributes, source=self.widget, dnd_source=self))
        self.txt_var = tkinter.StringVar()

        if self.widget_type == "Entry":
            self.widget["textvariable"] = self.txt_var #I love this line (see fix 001)
        else:
            self.widget["state"] = "normal"

        self.attributes = bUI.get_attributes(self.widget)
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
