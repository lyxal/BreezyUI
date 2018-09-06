# What's new in BreezyUI b1.4.0
* BreezyUI files are now able to be loaded (_Window sizing isn't avaliable yet, and will be made accessible later_)
* `Save` and `Export` dialogues now start in the last place a file was saved to
* Home screen shows whether or not width and height are valid when making a new GUI
* Cleaned up code files
* The box where the text for labels is now a `Text` widget
* Canvas width and height can now be changed
* Started adding a list manager widget (not usable yet, just in the code)
* Added the ability to give names to widgets, which are used in the exported code (verification of valid id name not implemented yet.)

# What's new in BreezyUI b1.3.1
* Made all classes external (i.e. placed them in the `Libraries` folder)
* Width and height entry boxes on home screen now flash when given invalid input
* Clicking new removes all objects on widget area

# What's new in BreezyUI b1.3.0
* _Everything new in pre b1.3.0_
* When exporting UIs, the python code that is generated is now fixed (There were issues with new lines)
* Added the `Canvas` core widget and customisable attributes
* Position of widget area is now relative to the size of the main area
* Changed how bUI files are created (i.e. the way they are formatted)

# What's new in BreezyUI pre b1.3.0
* Window size of new windows is now changeable
* Exporting code now goes to files, rather than console
* BreezyUI files are now able to be saved (_Loading will be made accessible later_)

# What’s new in BreezyUI b1.2.0
* The text in the `Entry` widget is now fully changeable
* Started adding home screen (Only `Create` button works)
* Exporting code only exports the changed attributes, and also places the widgets in their positions
* Created bug fix log to track all the bugs that were fixed before publishing
* When background colour of labels are changed, the label is updated accordingly

# What's new in BreezyUI b1.1.0
* Backwards compatibility for Python 2 started
* Attributes area window shows when widget right-clicked and hides when `Done` button clicked
* Changed the code to incorporate classes
* Added option to export python code for GUI (*TODO: Only export the necessary attributes*)
* Added more changeable attributes

# What's New in BreezyUI b1.0.0
* 3 core widgets added (`Label`, `Button` and `Entry`)
* Ability to edit the text displayed on widgets
* Started trying to make the background colours of widgets changeable (**WIP**)
