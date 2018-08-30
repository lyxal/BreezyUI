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

class Screen:
    def __init__(self, p_name, p_window):
        """
        Takes: Self, the name of the screen

        Does: Initialises the screen class

        Returns: Nothing
        """
        self.widgets = list()
        self.name = p_name
        self.window = p_window
        self.hidden = True

    def add_item(self, p_widget, p_row, p_column):
        """
        Takes: Self, a tkinter widget, a row number and a column number

        Does: Adds the item to the list of widgets to show

        Returns: Nothing
        """
        self.widgets.append([p_widget, p_row, p_column])
        
    def show(self):
        for item in self.widgets:
            item[0].grid(row=item[1], column=item[2])
        self.window.title(self.name)
        self.hidden = False
            
    def hide(self):
        for item in self.widgets:
            item[0].grid_forget()
        self.hidden = True

    def __iter__(self):
        return iter(self.widgets)

    def update_widget(self, count, new_x):
        self.widgets[count][1] = new_x

class ScreenXY(Screen):
    def add_item(self, p_widget, p_x, p_y):
        '''
        Takes: Self, a tkinter widget, and the x/y co-ordinates

        Does: Adds the item to the list of widgets to show

        Returns: Nothing
        '''

        
        self.widgets.append([p_widget, p_x, p_y, p_x, p_y])

    def show(self):
        for item in self.widgets:
            item[0].place(x=item[1], y=item[2])

        self.window.title(self.name)
        self.hidden = False

    def hide(self):
        for item in self.widgets:
            item[0].place_forget()
        self.hidden = True

