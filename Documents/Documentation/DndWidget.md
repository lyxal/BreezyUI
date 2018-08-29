# `DndWidget`
*A class allowing for draggable widgets to be created like tkinter widgets would*

`DndWidget`.**__init__**(*self*, *widget*, ***kwargs*)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`self`|self|The required self for class initialisation|
|`widget`|`str`|The type of widget the instance of `DndWidget` will be|
|`**kwargs`|`dict` [`str` : *mixed*]|The arguments to build the widget|

Creates a `DndWidget` object which stores a tkinter widget that is able to be dragged around. It also stores the id of the widget, the canvas position of the widget. Doesn't return anything.

`DndWidget`.**attach**(*self*, *canvas*, *x=10*, *y=10*)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`canvas`|`tkinter.Canvas`| The canvas which the `DndWidget` will be stored on|
|`x`|`int`|The x position where the `DndWidget` will be placed (optional)|
|`y`|`int`|The y position where the `DndWidget` will be placed (optional)|

Creates the draggable tkinter widget, places it at the specified co-ordinates (default `(10, 10)`) and enables it to be edited. Doesn't return anything.

`DndWidget`.**detach**(*self*)

Simply detaches the widget from the canvas and destroys it. Doesn't return anything.

`DndWidget`.**press**(*self*, *event*)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`event`|*Unknown*|The event given when the widget is pressed|

Updates the x and y position of the pointer and returns nothing.

`DndWidget`.**move**(*self*, *event*)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`event`|*Unknown*|The event given to the widget when moved|

Moves the widget on the canvas and updates the x and y position of the widget. Doesn't return anything.

`DndWidget`.**putback**(*self*)

Places the widget in its original position. Returns nothing.

`DndWidget`.**where**(*self*, *canvas*, *event*) -> `(int)`

|Parameter|Type|Description|
|:--------|:---|-----------|
|`canvas`|`tkinter.Canvas`|The canvas which the widget is on|
|`event`|*Unknown*|The event that is broadcasted when the function is called|

Calculates the relative position of the widget on the canvas it is on. Returns a tuple with the relative position of the widget.

`DndWidget`.**dnd_end**(*self*, *target*, *event*)

Compatibility function.
0
