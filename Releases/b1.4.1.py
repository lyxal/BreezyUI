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

#!/usr/bin/env python3

'''

Project: BreezyUI Version b1.5.0 (b1.5.0.py)
Author: JonoCode9374
Date Created: 6/9/2018
Description:

Many Python users who work with graphical interfaces know the pains of
designing and creating a Graphical User Interface with Python's built-in
graphics library tkinter (Tkinter in Python 2 and tkinter in Python 3) -
creating interfaces requires intense planning (getting the co-ordinates
for where each widget goes), lots of trial and error. This is what I
have personally experienced many times, making programs such as my SpamBot,
DocEdit and my Head Scruiteneer Program.

'''

###############################################################################
#Import section

import sys, os.path, _io
import re

if sys.version_info[0] == 2:
    import Tkinter as tkinter
    import Tkinter.dnd
    import tkFileDialog
else:
    import tkinter
    from tkinter import dnd #Accessed with `tkinter.dnd`. Provides drag'n'drop
                            #services
    import tkinter.filedialog


import functools
import tkinter.colorchooser as tkColor

sys.path.insert(0, '../Libraries') #Used for importing all custom libraries

import screens, bUI, DndWidget
import DndSpace, CoreWidget
###############################################################################
#Class section

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
            args = ", ".join([item[1:] if item[0] == "\\" else '"{0}"'.format(item) for item in args])


            construction = "{0}, {1}".format(construction, args)
            #At this point, construction would equal something like this:
            #tkinter.widget_type(attributes_area, args

        if kwargs:
            kwargs = ', '.join([str(x) + '=\'' + str(kwargs[x]) + "'" for x in kwargs])
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

        if widget_type in self.widgets or self.widgets == ["*"]:
            if self.name == "Display Text":
                self.option.delete("1.0", tkinter.END)
                self.option.insert("1.0", target_widget.cget("text"))

            elif self.name == "Background Colour":
                self.option["text"] = target_widget.cget("bg")
                self.option["bg"] = target_widget.cget("bg")

            elif self.name == "Border Colour":
                self.option["text"] = target_widget.cget("highlightbackground")

            elif self.name == "Canvas Height":
                self.option.delete(0, tkinter.END)
                self.option.insert(0, target_widget.cget("height"))

            elif self.name == "Canvas Width":
                    self.option.delete(0, tkinter.END)
                    self.option.insert(0, target_widget.cget("width"))

            elif self.name == "Object Name":
                    self.option.delete(0, tkinter.END)
                    self.option.insert(0, target_dndw.name)

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

###############################################################################
#Function section

def on_dnd_start(event, widget_type):
    '''
    This is invoked when a widget is dragged onto the main canvas.
    '''

    global dragged_widgets

    #Created the widget to be dragged
    if widget_type in ["Label", "Button", "Entry"]:
        dnd_widget = DndWidget.DndWidget(widget_type, text=widget_type, state='disabled', bg='#ffffff')

    else:
        dnd_widget = DndWidget.DndWidget(widget_type, bg="#ffffff", highlightbackground="#ffffff", relief="solid", bd=1)


    dragged_widgets.append(dnd_widget)
    dnd_widget.attach(widget_area.canvas)
    tkinter.dnd.dnd_start(dnd_widget, event)


def edit_attributes(event, source, dnd_source):
    global target_widget, target_dndw
    target_dndw = dnd_source
    target_widget = source

    attributes_area.geometry("+{0}+{1}".format(main_area.top.winfo_width(), widget_area.top.winfo_height() + 100))
    attributes_area.deiconify()

    for item in options:
        options[item].hide()

    for item in options:
        options[item].show(w_type(target_widget))



def hide_attributes():
    for item in options:
        options[item].hide()
    options["text"].option.delete("1.0", tkinter.END)
    options["placeholder"].option.delete("0", tkinter.END)
    attributes_area.withdraw()

def update_widget():
    global target_widget
    widget_type = w_type(target_widget)

    for option in options:
        option = options[option]
        if widget_type in option.widgets or option.widgets == ["*"]:
            if option.attribute == "":
                continue
            if option.attribute[0] != "$":
                target_widget.config({option.attribute : eval(option.var)})

            elif option.attribute == "$type":
                if entry_type.get() == "Password":
                    target_widget.config({"show" : "*"})
                else:
                    continue

            elif option.attribute == "$id":
                target_dndw.name = eval(option.var)

            elif option.attribute == "$placeholder":
                target_widget["state"] = "normal"
                target_dndw.txt_var.set(options["placeholder"].option.get())
                target_widget["state"] = "disabled"


            elif option.attribute == "$confirm":
                print("Confirmed")
    hide_attributes()
    target_widget = None


def choose_colour(event):
    global colour
    colour = tkColor.askcolor()[1]
    options["background"].option["bg"] = colour
    options["background"].option["text"] = colour

def choose_border_col(event):
    global border_colour
    border_colour = tkColor.askcolor()[1]
    options["canvas border colour"].option["bg"] = options["canvas border colour"].option["text"] = border_colour

def w_type(source):
    '''
    Takes:
    - source (a tkinter widget)

    Does:
    - See the the return section

    Returns:
    - The type of widget the option has
    '''

    widget_type = str(type(source))

    widget_type = widget_type[widget_type.find(".") + 1 : widget_type.find("'", widget_type.find("."))]

    return widget_type

def new(do_validate=True):
    if do_validate and validate_size(width_var.get(), height_var.get()):
            home_screen.hide()
            root.withdraw()
            main_area.show()
            main_area.top.geometry("{0}x{1}".format(width_var.get(), height_var.get()))
            widget_area.top.geometry("+{0}+60".format(width_var.get()))
            widget_area.show()
    else:
        home_screen.hide()
        root.withdraw()
        main_area.show()
        widget_area.show()

def back():
    home_screen.show()
    #TODO: Empty entry widgets
    root.deiconify()
    main_area.hide()
    widget_area.hide()
    attributes_area.withdraw()

    #Delete everything from screen
    for widget in dragged_widgets:
        widget.detach()

def validate_size(width, height):
    try:
        int(width)
        int(height)
    except ValueError:
        flash_red(5, [width_entry, height_entry])
        return False

    if width == "" or height == "":
        return False

    return True

def save_bUI_file():

    last_dir_f = open("../Resources/directory.txt")
    last_dir = last_dir_f.read().strip("\n")
    last_dir_f.close()

    root.filename = tkinter.filedialog.asksaveasfilename(initialdir = last_dir,title = "Select file",filetypes = (("python files","*.py"),("all files","*.*")))

    last_dir_f = open("../Resources/directory.txt", "w") #Truncate the file on purpose.
    last_dir_f.write(os.path.dirname(root.filename))
    last_dir_f.close()
    file = open(root.filename + ".bui", "w")
    file.write("[{0}, {1}]".format(width_var.get(), height_var.get()))

    #Generate the bUI file
    for widget in dragged_widgets:
        widget_config = {"id" : widget.name, "type" : widget.widget_type, "x" : widget.widget.winfo_x(), "y" : widget.widget.winfo_y(), "attributes" : bUI.changed_dict(widget.attributes, bUI.get_attributes(widget.widget))}

        if widget.widget_type == "Entry":
            widget_config["attributes"]["Placeholder"] = "'" + widget.widget.get() + "'"

        file.write(str(widget_config))

    #Add the bUI file to the recents list
    file = open("../Resources/recent.txt", "a")
    file.write(root.filename + ".bui" + "\n")
    file.close()

def load(source):
    '''
    Takes a .bUI file (file obj or str) and loads it into the page
    '''

    if type(source) is _io.TextIOWrapper:
        contents = source.read()

    elif type(source) in [str, bytes]:
        contents = source

    else:
        raise TypeError("Unknown type for source file")

    #[width, height]
    winfo_pattern = re.compile("\[(?P<width>\d+), (?P<height>\d+)\]")
    winfo_raw = re.match(winfo_pattern, contents).groupdict()



    #{"id" : str, "type" : str, "x" : int, "y" : int, "attributes" : {"name1" : "value1", "name2" : "value2", "name3" : "value3" ... "nameN" : "valueN"}}

    widget_pattern = re.compile("\{[^}]*?\}\}")
    widgets_raw = re.findall(widget_pattern, contents)

    widget_list = []

    structure = re.compile("\{\'id\': (?P<id>'(?:[^']|\\')*?'), \'type\': (?P<type>'(?:[^']|\\')*?'), \'x\': (?P<x>\d+), \'y\': (?P<y>\d+), \'attributes\': (?P<attributes>\{[^}]*\})\}")

    for widget in widgets_raw:
        widget_list.append(structure.match(widget).groupdict())

    new(False) #Go to the blank screen

    main_area.top.geometry("{0}x{1}".format(winfo_raw["width"], winfo_raw["height"]))
    widget_area.top.geometry("+{0}+60".format(winfo_raw["width"]))

    for widget in widget_list:
        args, kwargs = {}, {}
        t = eval("tkinter." + eval(widget["type"]) + "().config()")
        for attr in eval(widget["attributes"]):
            if attr in t:
                kwargs[attr] = eval(widget["attributes"])[attr]
            else:
                args[attr] = eval(widget["attributes"])[attr]
        args["name"] = widget["id"]

        kwarg = ", ".join(['{0} ="""{1}"""'.format(item, kwargs[item]) for item in kwargs])

        temp_widget = eval("DndWidget.DndWidget(eval(widget[\"type\"]), {0}, {1})".format(args, kwarg))



        temp_widget.name = eval(widget["id"])
        temp_widget.attach(main_area.canvas, int(widget["x"]), int(widget["y"]))
        dragged_widgets.append(temp_widget)

def goof():
    print("Fiddle Riddle Diddle Diddle")

def export():
    code = """

#############################################################
#     The following code was pre-generated by BreezyUI.     #
#Don't change any of the code if you don't know what it does#
#############################################################

import sys
if sys.version_info[0] == 2:
    import Tkinter as tkinter #backwards compatability
else:
    import tkinter

root = tkinter.Tk()
root.geometry("{0}x{1}") #Set the size of the window
    """.format(width_var.get(), height_var.get()) + "\n"
    for i in range(len(dragged_widgets)):
        widget = dragged_widgets[i]
        to_export = bUI.changed_dict(widget.attributes, bUI.get_attributes(widget.widget))
        code += "{0} = tkinter.{1}(root, {2})".format(widget.name, widget.widget_type, to_export) + "\n"

        code += "{0}.place(x={1},y={2})".format(widget.name, widget.widget.winfo_x(), widget.widget.winfo_y()) + "\n"

        if widget.widget_type == "Entry":
            if widget.widget.get():
                code += "{0}.insert(0, {1})".format(widget.name, widget.widget.get()) + "\n"

    code += "\n#################END OF GENERATED CODE#################"
    code += "\n#Add your code beneath this line"
    code += "\n\n\nroot.mainloop() #No more code after this"

    last_dir_f = open("../Resources/directory.txt")
    last_dir = last_dir_f.read().strip("\n")
    last_dir_f.close()

    root.filename = tkinter.filedialog.asksaveasfilename(initialdir = last_dir,title = "Select file",filetypes = (("python files","*.py"),("all files","*.*")))


    last_dir_f = open("../Resources/directory.txt", "w") #Truncate the file on purpose.
    last_dir_f.write(os.path.dirname(root.filename))
    last_dir_f.close()

    file = open(root.filename + ".py", "w")
    file.write(code)
    file.close()
    return

def flash_red(i, widgets):
    if i >= 0:
        temp = i - 1
        for widget in widgets:
            widget.configure({"background" : "red"})
        root.after(500, flash_white, temp, widgets)

def flash_white(i, widgets):
    if i >= 0:
        temp = i - 1
        for widget in widgets:
            widget.configure({"background" : "white"})
        root.after(500, flash_red, temp, widgets)

###############################################################################
#Window section
root = tkinter.Tk()
root.geometry("800x600")

main_area = DndSpace.DndSpace(root, 800, 600)
main_area.top.geometry("+1+60")
main_area.top.title("Untitled")

widget_area = DndSpace.DndSpace(root, 200, 600)
widget_area.top.geometry("+803+60")
widget_area.top.title("Widgets")

attributes_area = tkinter.Toplevel()
attributes_area.geometry("+803+160")
attributes_area.title("Edit Attributes")
attributes_area.withdraw()

###############################################################################
#Menu section

#Make all the menus
menu_bar = tkinter.Menu(root)
file_menu = tkinter.Menu(menu_bar, tearoff=0)
open_menu = tkinter.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=back)
file_menu.add_command(label="Save", command=save_bUI_file)
file_menu.add_command(label="Export", command=export)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.quit)

#Dynamically generate the open_menu
files = [line.strip("\n") for line in open("../Resources/recent.txt").readlines()]
for file in files:
    try:
        open_menu.add_command(label=file, command=functools.partial(load, open(file)))
    except FileNotFoundError:
        continue
        #TODO: Delete file from recents
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Recent Files", menu=open_menu)
root.config(menu=menu_bar)

###############################################################################
#Tkinter section

menu_bar = tkinter.Frame(root, height=600, width=200, bg="#878E88")
creation_bar = tkinter.Frame(root, height=200, width=600, bg="#C9CAC9")

size_label = tkinter.Label(root, text="Canvas Size (px): 0 px")

width_lbl = tkinter.Label(root, text="Width (px): ", bg="#C9CAC9", font=("Arial", 24))
height_lbl = tkinter.Label(root, text="Height (px): ", bg="#C9CAC9", font=("Arial", 24))

width_var = tkinter.StringVar()
height_var = tkinter.StringVar()

width_entry = tkinter.Entry(root, width=10, textvariable=width_var)
height_entry = tkinter.Entry(root, width=10, textvariable=height_var)

new_button = tkinter.Button(root, text="Create", command=new, width=25)

###############################################################################
#The Screen section
home_screen = screens.ScreenXY("BreezyUI", root)
home_screen.add_item(menu_bar, 0, 0)
home_screen.add_item(creation_bar, 200, 0)
home_screen.add_item(new_button, 200, 100)
home_screen.add_item(width_lbl, 210, 10)
home_screen.add_item(height_lbl, 205, 50)
home_screen.add_item(width_entry, 350, 15)
home_screen.add_item(height_entry, 350, 55)
home_screen.show()

###############################################################################
#Variable section

CoreWidget.widget_area = widget_area
CoreWidget.on_dnd_start = on_dnd_start
Option.attributes_area = attributes_area
DndWidget.edit_attributes = edit_attributes

colour = "#ffffff"
entry_type = tkinter.StringVar(root, "Plain")
border_colour = "#000000"

dragged_widgets = list() #of widgets
target_widget = None
target_dndw = None #Stores the DndWidget form of the target widget (dndw stands for DND Widget)

###############################################################################
#CoreWidget section

widgets = dict() #A dictionary to store all the widget objects which the clones will come from

widgets["label"] = CoreWidget.CoreWidget("Label", "Label", text="Label", bg="#ffffff")

widgets["button"] = CoreWidget.CoreWidget("Button", "Button", text="Button")
widgets["entry"] = CoreWidget.CoreWidget("Entry", "Entry")
widgets["canvas"] = CoreWidget.CoreWidget("Canvas", "Canvas", bd=1, relief="solid", highlightbackground="#ffffff", width=200, height=200)


widgets["canvas"].widget.create_text(100, 100, text="Canvas")

widgets["canvas"].widget.config({"bg" : "#ffffff"})

widgets["entry"].widget.delete(0, tkinter.END)
widgets["entry"].widget.insert(0, "Entry")

widgets["entry"].widget["state"] = "disabled"

#widgets["list frame"] = CoreWidget.CoreWidget("Listbox", "Canvas", bd=1, relief="solid", highlightbackground="#ffffff", width=200, height=100)


###############################################################################
#Option section

options = dict() #A dictionary to store all the attributes shown in the
                 #attributes area

options["text"] = Option("Display Text", "text", "options['text'].option.get('1.0','end-1c')", "Text", ["Label", "Button"], width=20, height=10, bd=3, relief="flat", highlightcolor="black")
options["background"] = Option("Background Colour", "background", "colour", "Label", ["Label", "Canvas"], borderwidth=2, relief="flat", highlightcolor="black")

options["background"].option.bind("<Button-1>", choose_colour)

options["entry type"] = Option("Type", "$type", "", "OptionMenu", ["Entry"], "\\entry_type", "Plain", "Password", "Numeric")

options["placeholder"] = Option("Placeholder", "$placeholder", "placeholder_text", "Entry", ["Entry"])

options["id"] = Option("Object Name", "$id", 'options["id"].option.get()', "Entry", ["*"])


options["canvas border colour"] = Option("Border Colour", "highlightbackground", "border_colour", "Label", ["Canvas"], text="#000000")

options["canvas border colour"].option.bind("<Button-1>", choose_border_col)

options["canvas height"] = Option("Canvas Height", "height", "options['canvas height'].option.get()", "Entry", ["Canvas"])

options["canvas width"] = Option("Canvas Width", "width", "options['canvas width'].option.get()", "Entry", ["Canvas"])


options["confirm"] = Option("", "$comfirm" , "", "Button", ["Label", "Button", "Entry", "Canvas"], text="Confirm")
options["confirm"].option["command"] = update_widget

###############################################################################
if __name__ == "__main__":
    root.mainloop()
