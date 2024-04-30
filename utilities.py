from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

def fileExplorer() -> str:

    """
    Opens a file explorer and allows the user to select a file
    :return: String with chosen path and file name
    """

    Tk().withdraw() # Prevent actual Tk window from appearing
    filename = askopenfilename()
    return os.path.normpath(filename) # Convert to proper path
