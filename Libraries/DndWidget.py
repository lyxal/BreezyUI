'''
MIT License

Copyright (c) 2018 JonoCode9374

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import tkinter, functools
import bUI, re

edit_attributes = None

class DndWidget():
    id_number = 0
    def __init__(self, widget_type, display_widget, args=None, *aargs, **kwargs):
        '''
        Takes:
        - self
        - widget_type [str] -- The type of widget that this instance will be
        - display_widget -- What the widget will show up as
        - args [dict] -- Attributes set when created (e.g. id, name -- things which don't respond to tkinter widget configuration)
        - kwargs [dict] -- Arguments used to build widget later on

        Does:
        - Initalises the instance of DndWidget

        Returns:
        - None
        '''
        self.widget_type, self.display = widget_type, display_widget
        self.canvas = self.widget = self._id =  None
        self.kwargs = kwargs
        self.name = "object{}".format(DndWidget.id_number)
        DndWidget.id_number += 1
        self.args = {}
        #self.aargs = ""
        if args:
            for attribute in args:
                exec("self.{0} = {1}".format(attribute, args[attribute]))
                self.args[attribute] = args[attribute]

        if len(aargs):
            self.aargs = ", ".join(

              [
                "{0}".format(arg)
                for arg in aargs
              ]

            ) #Innovative form of [value if condition else value for value in variable]
            self.aargs += ", "
        else:
            self.aargs = ""

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


        widget = eval(
        "tkinter.{0}(canvas, {1}{2})".format(self.display, self.aargs,
         ', '.join(
            [
                str(x) + '=\'\'\'' + str(self.kwargs[x]) + "\'\'\'"
                for x in self.kwargs
            ])))



        _id = canvas.create_window(x, y, window=widget, anchor="nw")
        self.canvas = canvas
        self.widget = widget
        self._id = _id
        self.x_off = 0
        self.y_off = 0
        widget.bind("<ButtonPress>", self.press)
        self.widget.bind("<Button-2>", functools.partial(edit_attributes, source=self.widget, dnd_source=self))
        self.txt_var = tkinter.StringVar()
        self.bool_var = tkinter.BooleanVar()

        if self.widget_type == "Entry":
            self.widget["textvariable"] = self.txt_var #I love this line (see fix 001)
            self.widget["state"] = "disabled"

            if "Placeholder" in dir(self):
                self.widget["state"] = "normal"
                self.widget.delete(0, tkinter.END)
                self.widget.insert(0, self.Placeholder)
                self.widget['state'] = "disabled"

        elif self.widget_type == "Checkbutton":
            self.widget["variable"] = self.bool_var
            self.widget["state"] = "disabled"

        elif self.widget_type == "OptionMenu":
            self.widget["state"] = tkinter.DISABLED
        else:
            self.widget["state"] = "normal"
            del self.txt_var
            del self.bool_var

        if self.widget_type == "Listbox":
            self.widget.create_text(100, 50, text="Listbox Object")

        elif self.widget_type == "Text":
            self.widget.create_text(100, 50, text="Text Object")



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
        widget.destroy()

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

    def __str__(self):
        return "DndWidget <<{0}>>".format(self.widget_type)
