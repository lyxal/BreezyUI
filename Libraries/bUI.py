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

def get_attributes(widget):
    attributes = {}
    for attribute in widget.keys():
        attributes[attribute] = widget.cget(attribute)

    return attributes

def changed_dict(dict_1, dict_2):
    #Returns a dictionary with all the keys from dict_1 that have their values changed in dict_2

    if list(dict_1) != list(dict_2):
        raise ValueError("Dictionaries given do not share the same keys")
    keys = list(dict_1)
    difference = {}
    for item in keys:
        if dict_1[item] != dict_2[item]:
            difference[item] = dict_2[item]

    return difference

#Testing
if __name__ == "__main__":
    import tkinter
    root = tkinter.Tk()
    widget = tkinter.Label(root, text="Before change")
    widget.pack() #Not _really_ needed for testing, but why not?
    before = get_attributes(widget)
    widget['text'] = "After change"
    widget['bg'] = "Green"
    after = get_attributes(widget)
    changed = changed_dict(before, after)
    print(changed)
