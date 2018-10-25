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


import sys, os.path, _io
import re
import tkinter
from tkinter import dnd #Accessed with `tkinter.dnd`. Provides drag'n'drop
                        #services
import tkinter.filedialog
import functools
import tkinter.colorchooser as tkColor
from typing import Dict, Any, List

sys.path.insert(0, '../Libraries') #Used for importing all custom libraries

import screens, bUI, DndWidget
import DndSpace, CoreWidget

class Option:
    row = 0 #Static class variable to determine which row to grid the option in
    def __init__(self, name : str, config_name : str, attr_var : str, widget_type : str, applicable_widgets : List[str], *args, **kwargs : Dict[str, Any]) -> None:

        ''' Represents a changeable option for a widget '''
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


    def show(self, widget_type : str) -> None:

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

            elif self.name == "Type":
                eval(self.var + ".set(target_dndw.type)")

            self.label.grid(row=self.x, column=0)
            self.option.grid(row=self.x, column=1)

    def hide(self) -> None:
        self.label.grid_forget()
        self.option.grid_forget()
def on_dnd_start(event, display_widget, widget_type):
    '''
    This is invoked when a widget is dragged onto the main canvas.
    '''

    global dragged_widgets

    #Created the widget to be dragged
    if widget_type in ["Label", "Button", "Entry", "Checkbutton"]:
        args = {}
        if widget_type == "Entry":
            args = {"type" : "'Plain'"}

        if widget_type == "Checkbutton":
            args = {"state" : False}
        dnd_widget = DndWidget.DndWidget(widget_type, display_widget, args, text=widget_type, state='disabled', bg='#ffffff')

    elif widget_type == "Canvas":
        dnd_widget = DndWidget.DndWidget(widget_type, display_widget, bg="#ffffff", highlightbackground="#ffffff", relief="solid", bd=1)

    elif widget_type == "Listbox":
        dnd_widget = DndWidget.DndWidget(widget_type, display_widget, {"items" : "[]"}, bg="#ffffff", highlightbackground="#ffffff", relief="solid", bd=1, height=100, width=200)

    elif widget_type == "Text":
        dnd_widget = DndWidget.DndWidget(widget_type, display_widget, {"height" : 100, "width" : 200}, bg="#ffffff", highlightbackground="#ffffff", relief="solid", bd=1, height=100, width=200)

    elif widget_type == "OptionMenu":
        dnd_widget = DndWidget.DndWidget(widget_type, display_widget, {}, "tkinter.StringVar(canvas, 'OptionMenu')", "'OptionMenu'")

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
        options[item].show(target_dndw.widget_type)
def hide_attributes():
    for item in options:
        options[item].hide()
    options["text"].option.delete("1.0", tkinter.END)
    options["placeholder"].option.delete("0", tkinter.END)
    attributes_area.withdraw()
def update_widget():
    global target_widget
    widget_type = target_dndw.widget_type

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

            elif option.attribute == "$command":
                 exec("def {0}(): pass".format(eval(option.var)))
                 target_widget.config(command="{0}".format(eval(option.var)))

            elif option.attribute == "$id":
                if bUI.is_valid_name(eval(option.var)):
                    target_dndw.name = eval(option.var)

            elif option.attribute == "$items":
                del target_dndw.items[:]
                target_dndw.items.append(reversed(eval(option.var)))

            elif option.attribute == "$placeholder":
                target_widget["state"] = "normal"
                target_dndw.txt_var.set(options["placeholder"].option.get())
                target_widget["state"] = "disabled"

            elif option.attribute == "$state":
                target_widget["state"] = "normal"
                target_dndw.bool_var.set(eval(option.var).get())
                target_widget["state"] = "disabled"

            elif option.attribute == "$t_width":
                target_widget["width"] = eval(option.var)
                target_dndw.width = eval(option.var)

            elif option.attribute == "$t_height":
                target_widget["height"] = eval(option.var)
                target_dndw.height = eval(option.var)

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

    widget_type = str(type(source))

    widget_type = widget_type[widget_type.find(".") + 1 : widget_type.find("'", widget_type.find("."))]

    return widget_type
def init_ui():
    home_screen.hide()
    root.withdraw()
    main_area.show()

    main_width, main_height = main_area.top.winfo_width(), main_area.top.winfo_height()

    if width_var.get() != "": #Tests to see if the window was loaded from a file or not
        canv_width, canv_height = int(width_var.get()), int(height_var.get())

        main_area.canvas.config(width=canv_width, height=canv_height)
        main_area.top.minsize(canv_width, canv_height)

    main_area.frame.pack(fill="none", expand="True")
    main_area.top.geometry("1001x871")
    main_area.top.bind("<Configure>", resize)
    widget_area.top.geometry("430x870+{0}+1".format(main_width + 1))
    widget_area.show()
def new(do_validate=True):

    if do_validate:
        if validate_size(width_var.get(), height_var.get()):
            init_ui()
            return

        return

    for widget in dragged_widgets:
        widget.detach()
    init_ui()
def resize(event):

    main_width, main_height = main_area.top.winfo_width(), main_area.top.winfo_height()

    widget_area.top.geometry("+{0}+0".format(main_width + 1))
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

    with open("../Resources/directory.txt") as last_directory:
        directory = last_directory.read().strip()

    bui_filetypes = (("BreezyUI Files", "*.bui"), ("all files", "*.*"))

    root.filename = tkinter.filedialog.asksaveasfilename(initialdir=directory, title="Select file", filetypes=bui_filetypes)

    with open("../Resources/directory.txt", "w") as last_directory:
        last_directory.write(os.path.dirname(root.filename))

    save_file = open(root.filename + ".bui", "w")
    contents = "[{0}, {1}]".format(width_var.get(), height_var.get())


    #Generate the bUI file
    for widget in dragged_widgets:

        widget_config = {
            "id" : widget.name,
            "display" : widget.display,
            "type" : widget.widget_type,
            "x" :  widget.widget.winfo_x(),
            "y" : widget.widget.winfo_y(),
            "attributes" : bUI.changed_dict(widget.attributes, bUI.get_attributes(widget.widget))
        }

        if widget.args != {}:
            for arg in widget.args:
                widget_config["attributes"][arg] = widget.args[arg]

        if widget.widget_type == "Entry":
            widget_config["attributes"]["Placeholder"] = "'" + widget.widget.get() + "'"

        if widget.widget_type in ["Text", "Listbox"]:
            widget_config["attributes"]["width"] = 200
            widget_config["attributes"]["height"] = 100
            widget_config["attributes"]["relief"] = "solid"
            widget_config["attributes"]["bd"] = 1

        if widget.widget_type == "OptionMenu":
            widget_config["attributes"]["value"] = "'{0}'".format(widget["text"])



        contents += str(widget_config)

    save_file.write(contents);save_file.close()

    #Add the bUI file to the recents list
    file = open("../Resources/recent.txt", "a")
    file.write(root.filename + ".bui" + "\n")
    file.close()
def load(source):
    '''
    Takes a .bUI file (file obj or str) and loads it into the page
    '''

    if type(source) is _io.TextIOWrapper: #Test to see if the source is a file object
        contents = source.read()

    elif type(source) in [str, bytes]:
        contents = source

    else:

        raise TypeError("Unknown type for source file")


    #Get the window information
    winfo = {"pattern" : re.compile("\[(?P<width>\d+), (?P<height>\d+)\]")}
    winfo["raw"] = re.match(winfo["pattern"], contents).groupdict()

    #Now, get all the widgets
    widgets = {"pattern" : re.compile("\{[^}]*?\}\}")}
    widgets["raw"] = re.findall(widgets["pattern"], contents)
    widget_list = []

    structure = re.compile("\{\'id\': (?P<id>'(?:[^']|\\')*?'), \'display\': (?P<display>'(?:[^']|\\')*?'), \'type\': (?P<type>'(?:[^']|\\')*?'), \'x\': (?P<x>\d+), \'y\': (?P<y>\d+), \'attributes\': (?P<attributes>\{[^}]*\})\}")

    for widget in widgets["raw"]:
        widget_list.append(structure.match(widget).groupdict())

    new(False) #Go to the blank screen and not validate any sizes

    main_area.canvas.config(width=int(winfo["raw"]["width"]))
    main_area.canvas.config(height=int(winfo["raw"]["height"]))

    main_area.top.minsize(int(winfo["raw"]["width"]), int(winfo["raw"]["height"]))

    widget_area.top.geometry("+{0}+0".format(winfo["raw"]["width"]))

    for widget in widget_list:
        args, kwargs = {}, {}
        widget_attrs = eval("tkinter." + eval(widget["type"]) + "().config()")
        for attr in eval(widget["attributes"]):
            if attr in widget_attrs:
                kwargs[attr] = eval(widget["attributes"])[attr]
            else:
                args[attr] = eval(widget["attributes"])[attr]

        args["name"] = widget["id"]

        kwarg = ", ".join(['{0}="""{1}"""'.format(item, kwargs[item]) for item in kwargs])

        temp_widget = eval("DndWidget.DndWidget(eval(widget[\"type\"]), {0}, {1}, {2})".format(widget["display"], args, kwarg))

        temp_widget.name = eval(widget["id"])
        temp_widget.attach(main_area.canvas, int(widget["x"]), int(widget["y"]))
        dragged_widgets.append(temp_widget)
def export(event=None):
    code = ""
    code += bUI.START_COMMENT
    code += "import sys, bUI\n"
    code += "if sys.version_info[0] == 2:\n"
    code += "    import Tkinter as tkinter\n"
    code += "else:\n"
    code += "    import tkinter\n"
    code += "root = tkinter.Tk()\n"
    code += "root.geometry('{0}x{1}')\n".format(main_area.canvas.winfo_width(), main_area.canvas.winfo_height())

    for index in range(len(dragged_widgets)):
        widget = dragged_widgets[index]
        changed_attrs = bUI.changed_dict(widget.attributes, bUI.get_attributes(widget.widget))

        if widget.widget_type != "Text":
            code += "{0} = tkinter.{1}(root, {2})\n".format(
            widget.name,
            widget.widget_type,
            changed_attrs
            )

        if widget.widget_type == "Entry":
            if widget.widget.get():
                code += "{0}.insert(0, '{1}')\n".format(
                widget.name,
                widget.widget.get()
                )

        elif widget.widget_type == "Listbox":
            if len(widget.items):
                for item in widget.items[0].split("\n"):
                    code += "{0}.insert(0, '{1}')\n".format(widget.name, item)

        elif widget.widget_type == "Text":
            code += "{0} = bUI.Textbox(root, {1}, {2}, {3})\n".format(
            widget.name,
            widget.width,
            widget.height,
            changed_attrs
            )


        code += "{0}.place(x={1}, y={2})\n".format(
        widget.name,
        widget.widget.winfo_x(),
        widget.widget.winfo_y()
        )

    code += bUI.END_COMMENT
    code += "\n\n\n\n\n\n\nroot.mainloop() #Ensure that you keep this line, as it was added by BreezyUI"

    with open("../Resources/directory.txt") as last_directory:
        directory = last_directory.read().strip()

    root.filename = tkinter.filedialog.asksaveasfilename(initialdir=directory,
    title="Select file", filetypes =(("python files","*.py"),("all files","*.*")))


    with open("../Resources/directory.txt", "w") as last_directory:
        last_directory.write(os.path.dirname(root.filename))

    import shutil
    shutil.copy("../Libraries/bUI.py", os.path.dirname(root.filename))
    file = open(root.filename + ".py", "w")
    file.write(code)
    file.close()
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
def open_bui(event=None):
    last_dir_f = open("../Resources/directory.txt")
    last_dir = last_dir_f.read().strip("\n")
    last_dir_f.close()
    ftypes = [('BreezyUI Files', '*.bui'), ('All files', '*')]
    file = tkinter.filedialog.askopenfilename(initialdir=last_dir, filetypes=ftypes)
    load(open(file))
def size(area):
    if area == "main":
        print(main_area.top.winfo_width(), main_area.top.winfo_height())

    elif area == "widget":
        print(widget_area.top.winfo_width(), widget_area.top.winfo_height())

    elif area == "main canvas":
        print(main_area.canvas.winfo_width(), main_area.canvas.winfo_height())
def goof(): print("Fiddle diddle riddle diddle.")

###############################################################################
#Window section
root = tkinter.Tk()
root.geometry("800x600")

main_area = DndSpace.DndSpace(root, 1001, 871, "main")

main_area.top.geometry("+1+0")
main_area.top.title("Main Area")
main_area.top.config(bg="#878E88")
main_area.top.maxsize(width=1001, height=871)

widget_area = DndSpace.DndSpace(root, 800, 600, "widget area")
widget_area.top.geometry("+1001+0")
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
test_menu = tkinter.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=back)
file_menu.add_command(label="Open", command=open_bui)
file_menu.add_separator()
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

test_menu.add_command(label="Main Area Size", command=functools.partial(size, "main"))
test_menu.add_command(label="Widget Area Size", command=functools.partial(size, "widget"))
test_menu.add_command(label="Main Canvas Size", command=functools.partial(size, "main canvas"))

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Recent Files", menu=open_menu)
menu_bar.add_cascade(label="Development Options", menu=test_menu)
root.config(menu=menu_bar)

main_area.top.bind('<Command-e>', export)

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

sidebar_btn_frame = tkinter.Frame(root, width=200, height=50, bg="#878E88")
sidebar_btn_frame.pack_propagate(0) #https://stackoverflow.com/a/16363832/9363594

sidebar_btn = tkinter.Label(sidebar_btn_frame, text="Load .bui File", bg="#878E88", fg="white", width=200)
sidebar_btn.pack()
sidebar_btn.bind("<Button-1>", open_bui)

logo = tkinter.Label(root, text="BreezyUI", bg="#878E88", fg="white", font=("Sans", 40, "bold"))

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
home_screen.add_item(sidebar_btn_frame, 0, 70)
home_screen.add_item(logo, 14, 0)
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
checkbox_state = tkinter.BooleanVar(root, False)


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

widgets["list frame"] = CoreWidget.CoreWidget("Listbox", "Canvas", bd=1, relief="solid", highlightbackground="#ffffff", width=200, height=100)

widgets["list frame"].widget.create_text(100, 50, text="Listbox")

widgets["text"] = CoreWidget.CoreWidget("Text", "Canvas", width=200, height=100, bd=1, relief="solid", highlightbackground="#ffffff")

widgets["text"].widget.create_text(100, 50, text="Textbox")

widgets["checkbox"] = CoreWidget.CoreWidget("Checkbutton", "Checkbutton", text="Checkbutton")

widgets["OptionMenu"] = CoreWidget.CoreWidget("OptionMenu", "OptionMenu", "$tkinter.StringVar(widget_area.canvas, \"OptionMenu\")", "OptionMenu")

widgets["OptionMenu"].widget["state"] = tkinter.DISABLED

###############################################################################
#Option section

options = dict() #A dictionary to store all the attributes shown in the
                 #attributes area

options["text"] = Option("Display Text", "text", "options['text'].option.get('1.0','end-1c')", "Text", ["Label", "Button"], width=20, height=10, bd=3, relief="flat", highlightcolor="black")
options["background"] = Option("Background Colour", "background", "colour", "Label", ["Label", "Canvas"], borderwidth=2, relief="flat", highlightcolor="black")

options["background"].option.bind("<Button-1>", choose_colour)

options["entry type"] = Option("Type", "$type", "entry_type", "OptionMenu", ["Entry"], "\entry_type", "Plain", "Password", "Numeric")

options["button function"] = Option("Callback", "$command", "options['button function'].option.get()", "Entry", ["Button"])

options["placeholder"] = Option("Placeholder", "$placeholder", "placeholder_text", "Entry", ["Entry"])

options["id"] = Option("Object Name", "$id", 'options["id"].option.get()', "Entry", ["*"])

options["canvas border colour"] = Option("Border Colour", "highlightbackground", "border_colour", "Label", ["Canvas"], text="#000000")

options["canvas border colour"].option.bind("<Button-1>", choose_border_col)

options["canvas height"] = Option("Canvas Height", "height", "options['canvas height'].option.get()", "Entry", ["Canvas"])

options["canvas width"] = Option("Canvas Width", "width", "options['canvas width'].option.get()", "Entry", ["Canvas"])

options["list items"] = Option("Items", "$items", "options['list items'].option.get('1.0', 'end-1c')", "Text", ["Listbox"], width=20, height=30) #Funny thing is... these don't actually have to change the look of any widgets in the main area.
#The list items are only dealt with when saving/exporting files!

options["textbox width"] = Option("Width", "$t_width", "options['textbox width'].option.get()", "Entry", ["Text"])

options["textbox height"] = Option("Height", "$t_height", "options['textbox height'].option.get()", "Entry", ["Text"])

options["checkbox default state"] = Option("Default State", "$state", "checkbox_state", "Checkbutton", ["Checkbutton"])

#options["menu options"] = Option("Options", )
options["confirm"] = Option("", "$comfirm" , "", "Button", ["*"], text="Confirm")
options["confirm"].option["command"] = update_widget



###############################################################################
if __name__ == "__main__":
    root.mainloop()
