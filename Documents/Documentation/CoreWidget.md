# `CoreWidget`

*A class that is a place that new widgets are dragged from*

`CoreWidget`.**\_\_init\_\_**(_self_, _widget\_type_, _**kwargs_)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`self`|self|The required self for class initialisation|
|`widget_type`|`str`|The type of `tkinter` widget that the instance will be|
|`**kwargs`|`[str : Mixed]`|The arguments used to configure the construction of the widget|

<hr>

`CoreWidget`.**widget_type**
_Type: `str`_

Contains the widget type that the core widget is

<hr>

`CoreWidget`.**widget**
_Type: `tkinter` widget_

Contains the `tkinter` representation of the widget

<hr>

(_static variable_) `CoreWidget`.**row**
_Type: `int`_

This variable is used to determine which row the next `CoreWidget` object will be placed in the widget area. When a new instance is created, this variable is incremented by 1 if the column number (see below) is 1. Otherwise, it stays the same.

<hr>

(_static variable_) `CoreWidget`.**column**
_Type: `int`_

Much like the `row` variable, this variable is used to determine which column the next `CoreWidget` object will be placed in the widget area. When a new instance is created, this variable is set to 1 if it is 0, and set to 0 if it is 1.
