# `DndSpace`

*A class representing a space where draggable widgets can be moved around freely.*

`DndSpace`.**\_\_init\_\_**(_self_, _root_, _width_, _height_)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`self`|self|The self needed for initialisation|
|`root`|`tkinter.Tk`|The root window which the space will be on|
|`width`|`int`|The width of the canvas|
|`height`|`int`|The height of the canvas|

Creates a `DndSpace` object. Returns nothing.

<hr>

`DndSpace`.**show**(_self_)

Shows the `DndSpace` (makes it visible). Returns nothing

<hr>

`DndSpace`.**hide**(_self_)

Hides the `DndSpace`. Returns nothing

<hr>

`DndSpace`.**dnd_accept**(_self_, _source_, _event_)

Compatibility function

<hr>

`DndSpace`.**dnd_enter**(_self_, _source_, _event_)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`source`|`tkinter` widget| The widget being moved onto the `DndSpace`|
|`event`|_Unknown_|_Unknown_|

Sets up the widget for when it is dragged onto the `DndSpace`. Returns nothing

<hr>

**See rest of class for rest of documentation**
