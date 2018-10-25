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

class DndSpace:
    def __init__(self, root, width, height, name=None):
        '''
        Takes:
        - self
        - root [tkinter.Tk()] -- the window which the space will be on
        - width [int] -- the width of the canvas
        - height [int] -- the height of the canvas
        - name [str] -- The name of the DndSpace

        Does:
        - Intalises this instance of DndSpace

        Returns:
        - None
        '''

        self.top = tkinter.Toplevel(root)
        self.name = name
        self.top.withdraw()
        self.width = width
        self.height = height
        #self.top.geometry("{}")
        self.frame = tkinter.Frame(self.top, width=width, height=height)
        self.canvas = tkinter.Canvas(self.frame, width=width, height=height)
        self.frame.place(x=0, y=0)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.dnd_accept = self.dnd_accept
        

    def show(self):
        self.top.deiconify()

    def hide(self):
        self.top.withdraw()

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

    #I won't comment the next few functions, as I don't quite understand them in
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
