from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

def fileExplorer() -> str:

    Tk().withdraw() # Prevent actual Tk window from appearing
    filename = askopenfilename()
    return os.path.normpath(filename) # Convert to proper path