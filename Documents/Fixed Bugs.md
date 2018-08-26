<!-- This is a document where I go to feel happy -->
# 001 -- Changing one `Entry` changes another
## Description
When an `Entry` was dragged onto the screen and it's placeholder text was changed, it would go and change all of the other placeholder texts in the other entries on the screen.

## Solution
* Create a `StringVar()` for each instance of `DndWidget`.
* On creation, if the `DndWidget` was an `Entry`, set the `textvariable` of the `Entry` to the `StringVar()`.
* When the widget was right clicked to change attributes, store both the target widget object **and** the target `DndWidget` object.
* When the placeholder text was changed, execute the following line:
```python
target_dndw.txt_var.set(options["placeholder"].option.get()
```
