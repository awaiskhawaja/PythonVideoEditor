from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import typing

def fileExplorer(multiple: bool=False) -> typing.Union[typing.List[str], str, None]:

    """
    Opens a file explorer and allows the user to select a file
    :param multiple: If multiple items can be selected.
    :return: String with chosen path and file name. If multiple=True, returns a list instead
    """

    Tk().withdraw() # Prevent actual Tk window from appearing
    filename = askopenfilename(multiple=multiple)

    if multiple:
        if len(filename) == 0: # "Cancel" pressed
            return None
        return [os.path.normpath(f) for f in filename] # Convert each selected file to a path

    else:
        if filename == "": # "Cancel" pressed
            return None
        return os.path.normpath(filename) # Convert to proper path
