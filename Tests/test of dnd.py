from tkinter import dnd as Tkdnd
import tkinter

#How is `from tkinter import dnd` different to `import tkinter`?
#Fine, well I'll tell you. It's because `from tkinter import dnd`
#only imports one file, if you know what I mean, while
#`import tkinter` imports **ALL** of tkinter.

import functools

#Create a base widget that is dnd'able

'''self.widget = eval('tkinter.{widget_name}({*args})')

self.widget = tkinter.widget_name(*args)'''

class DndWidget():
    def __init__(self, name, **kwargs):
        self.name = name
        self.canvas = self.widget = self.id = None
        self.args = kwargs

    def attach(self, canvas, x=10, y=10):
        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return

        #This is the line to change to make different widget types

        widget = eval('tkinter.{0}(canvas, {1})'.format(self.name, ', '.join([str(x) + '=' + self.args[x] for x in self.args])))
        _id = canvas.create_window(x, y, window=widget, anchor="nw")
        self.canvas = canvas
        self.widget = widget
        self.id = _id
        self.x_off = 0
        self.y_off = 0
        widget.bind("<ButtonPress>", self.press)
        self.widget.bind("<Button-2>", functools.partial(edit, source=self.widget))


    def detach(self):
        canvas = self.canvas
        if not canvas:
            return
        _id = self.id
        widget = self.widget
        self.canvas = self.widget = self.id = None
        canvas.delete(_id)
        widget.destroy()

    def press(self, event):
        if tkinter.dnd.dnd_start(self, event):
            # where the pointer is relative to the widget widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self.id)

    def move(self, event):
        x, y = self.where(self.canvas, event)
        self.canvas.coords(self.id, x, y)

    def putback(self):
        self.canvas.coords(self.id, self.x_orig, self.y_orig)

    def where(self, canvas, event):
        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x - self.x_off, y - self.y_off

    def dnd_end(self, target, event):
        pass


class DndSpace:

    def __init__(self, root, width, height):
        self.top = tkinter.Toplevel(root)
        self.canvas = tkinter.Canvas(self.top, width=width, height=height)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.dnd_accept = self.dnd_accept

    def dnd_accept(self, source, event):
        return self

    def dnd_enter(self, source, event):
        #source.widget.lift()
        self.canvas.focus_set() # Show highlight border
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = source.canvas.bbox(source.id)
        dx, dy = x2-x1, y2-y1
        self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
        self.dnd_motion(source, event)

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

def on_dnd_start(Event, Type):
        """
        This is invoked by InitiationObject to start the drag and drop process.
        """
        #Create an object to be dragged
        ThingToDrag = DndWidget(Type, text='"Change me"')
        ThingToDrag.attach(widgets.canvas)
        #Pass the object to be dragged and the event to Tkdnd
        Tkdnd.dnd_start(ThingToDrag,Event)

def edit(event, source):
    global s
    s = source
    options_text_lbl.pack()
    options_text.pack()
    options_button.pack()
    
def close():
    options_text_lbl.pack_forget()
    options_text.delete("0", tkinter.END)
    options_text.pack_forget()
    options_button.pack_forget()
    

def update_widget():
    global s
    s.config({"text":options_text.get()})
    close()
    
def foo():
    print("Get off me! That's my ear!")


s = None

root = tkinter.Tk()
root.geometry("+1+1")
root.withdraw()

home = DndSpace(root, 800, 600)
home.top.geometry("+1+60")

widgets = DndSpace(root, 200, 600)
widgets.top.geometry("+803+60")

text_orig = tkinter.Label(widgets.canvas, text="Label")
text_orig.pack()
text_orig.bind('<ButtonPress>', functools.partial(on_dnd_start, Type="Label"))

button_orig = tkinter.Button(widgets.canvas, text="Button")
button_orig.pack()
button_orig.bind('<ButtonPress>', functools.partial(on_dnd_start, Type="Button"))

entry_fill = tkinter.StringVar(root, value="Entry")
entry_orig = tkinter.Entry(widgets.canvas, textvariable=entry_fill)
entry_orig.pack()
entry_orig.bind('<ButtonPress>', functools.partial(on_dnd_start, Type="Entry"))

options = tkinter.Tk()
options.geometry("+803+160")
options_text_lbl = tkinter.Label(options, text="Display Text")
options_text = tkinter.Entry(options)
options_button = tkinter.Button(options, text="confirm", command=update_widget)
root.mainloop()

