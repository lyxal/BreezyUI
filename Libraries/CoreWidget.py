import tkinter, functools

widget_area = None

on_dnd_start = None

class CoreWidget:

    row = column = 0

    def __init__(self, widget_type, **kwargs):
        '''
        Takes:
        - self
        - widget_type -- The type of tkinter widget that the instance will be
        '''

        self.widget_type = widget_type
        self.widget = eval("tkinter.{0}(widget_area.canvas, {1})".format(widget_type, ', '.join([str(x) + '=' + kwargs[x] for x in kwargs])))

        self.widget.grid(row=CoreWidget.row, column=CoreWidget.column)

        if CoreWidget.column == 1:
            CoreWidget.row += 1
            CoreWidget.column = 0
        else:
            CoreWidget.column = 1

        self.widget.bind("<ButtonPress>", functools.partial(on_dnd_start, widget_type=widget_type))
