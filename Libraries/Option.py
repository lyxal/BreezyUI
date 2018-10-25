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

import tkinter

attributes_area = None

class Option:
    row = 0

    def __init__(self, name, config_name, attr_var, widget_type, applicable_widgets, *args, **kwargs):
        '''
        Takes:
        - self
        - name [str] -- The name of this option
        - config_name [str] -- The config attribute this affects
        - attr_var [str] -- The variable which the attribute is stored in
        - widget_type [str] -- The type of widget this option is
        - applicable_widgets [[str]] -- The widgets this option shows for
        - **kwargs -- The arguments to construct the widget

        Does:
        - Initalises this instance of option

        Returns:
        - None

        '''

        self.name = name
        self.attribute = config_name
        self.var = attr_var

        #Create the label and widget for this option
        self.label = tkinter.Label(attributes_area, text=name)

        construction = "tkinter.{0}(attributes_area".format(widget_type)

        if args:
            args = ", ".join([str(x) for x in args])
            construction = "{0}, {1}".format(construction, args)
            #At this point, construction would equal something like this:
            #tkinter.widget_type(attributes_area, args

        if kwargs:
            kwargs = ', '.join([str(x) + '=' + kwargs[x] for x in kwargs])
            construction = "{0}, {1}".format(construction, kwargs)
            #If the args wasn't empty, construction would look like this: tkinter.widget_type(attributes_area, args, kwargs

        construction += ")"


        self.option = eval(construction)

        self.x = Option.row
        Option.row += 1

        self.widgets = applicable_widgets


    def show(self, widget_type):
        '''
        Takes:
        - self
        - widget_type [str] -- The type of widget being shown

        Does:
        - Shows the widget in the appropriate location if it is for a widget it supports

        Returns:
        - None
        '''



        if widget_type in self.widgets:
            if self.name == "Display Text":
                self.option.delete(0, tkinter.END)
                self.option.insert(0, target_widget.cget("text"))

            elif self.name == "Background Colour":
                self.option["text"] = target_widget.cget("bg")

            elif self.name == "Border Colour":
                self.option["text"] = target_widget.cget("highlightbackground")

            self.label.grid(row=self.x, column=0)
            self.option.grid(row=self.x, column=1)

    def hide(self):
        '''
        Takes:
        - self

        Does:
        - Hides the widget using `.grid_forget()`

        Returns:
        - None
        '''

        self.label.grid_forget()
        self.option.grid_forget()
