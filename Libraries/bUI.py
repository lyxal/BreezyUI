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
