# `Option`

_A class that stores changeable attributes of widgets_

`Option`.**\_\_init\_\_**(_self_, _name_, _config\_name_, _attr\_var_, _widget_type_, _applicable\_widgets_, _\*args_, _\*\*kwargs_)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`self`|self|The required self for class initialisation|
|`name`|`str`|The name of the option (e.g. "Type")|
|`config_name`|`str`|The name that the option can be referred to as when updating the widget (e.g. "$text")|
|`attr_var`|`str`|The variable which the value for the option is stored (must be the variable name in a string)|
|`widget_type`|`str`|The widget type that this option will be shown as (e.g. the Text option will be displayed as an `Entry`)|
|`applicable_widgets`|`[str]`|The widgets for which this option applies to (e.g. the background colour attribute may only apply to `Label`s and `Canvas`es)|
|`*args`|`(Mixed)`|Positional arguments used to configure the widget (the one that displays in the attribute area)|
|`**kwargs`|`[str : Mixed]`|Keyword arguments used to configure the widget (the one that displays in the attribute area)|
<hr>
`Option`.**show**(_self_, _widget\_type_)

|Parameter|Type|Description|
|:--------|:---|-----------|
|`widget_type`|`str`|The type of widget whose attributes are being changed|

If the widget being edited is of a type which this option supports, then the option is shown, otherwise, nothing happens. Nothing is returned from this function.
<hr>
`Option`.**hide**(_self_)

Hides the option using `.grid_forget()`. Returns nothing.
