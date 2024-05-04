import pygame
import typing
import warnings

"""
Dictionary of themes.
Each theme has a list of colours associated with it, that are used by the different GUI elements.

buttons: text, normal, hover, clicked
"""
allThemes = {
    "basic": [(0, 0, 0), (255, 255, 255), (200, 200, 200), (100, 100, 100)],
    "dark": [(200, 200, 200), (50, 50, 50), (75, 75, 75), (100, 100, 100)]
}

# Default style parameters for button class
buttonDefaults: dict = {
    "font": "agency fb",
    "size": 20,
    "border": False,
    "border-width": 2,
    "padding-width": 50,
    "padding-height": 20
}

buttonListDefaults: dict = {
    "spacing": 0
}

# Local version of mouse data that all GUI objects can use
local_mx: int = 0
local_my: int = 0
local_mp: bool = False
local_m_down: bool = False

def local_mtouch(tx: int, ty: int, tw: int, th: int) -> bool:

    """
    Detects if the mouse is hovering over a certain area.
    """

    global local_mx, local_my

    t = False
    if tx < local_mx < tx + tw:
        if ty < local_my < ty + th:
            t = True
    return t
def updateLocals(x: int, y: int, mp: bool, m_down: bool) -> None:

    """
    Used to update local version of mouse data, to be used by all other GUI objects.

    :param x: Mouse x
    :param y: Mouse y
    :param mp: True if mouse LMB pressed
    :param m_down: True on single frame mouse LMB clicked
    """

    global  local_mx, local_my, local_mp, local_m_down

    local_mx = x
    local_my = y
    local_mp = mp
    local_m_down = m_down

class button:

    """
    Button object. Displays text and can call a function when clicked.
    Changes colour when hovered over and clicked.
    Can specify a range of style parameters to customise appearance.
    """

    def __init__(self, text: str, theme: str, pos: typing.Tuple[int, int], function: typing.Callable = None, style: dict = None) -> None:

        """
        Creates a new button GUI object.

        :param text: Text to display on button.
        :param theme: Colour theme to use, key from allThemes dictionary.
        :param pos: Coordinate of top-left corner of button.
        :param function: Function to call when button clicked.
        :param style: A dictionary with customisable style parameters.
        """

        global allThemes

        self.text: str = text
        self.theme: str = theme
        self.function: typing.Callable = function
        self.pos: typing.Tuple[int, int] = pos

        if not self.theme in allThemes:
            warnings.warn(f"{self.theme} theme does not exist! Defaulting to basic theme.")
            self.theme = "basic"

        if style is None:
            self.style: dict = {}
        else:
            self.style: dict = style

        self.width: int = 0
        self.height: int = 0

        self.surfaces: typing.Dict[str, pygame.Surface] = {} # Different surfaces for different states of interaction

        self.state: str = "normal"
        self.isPressed: bool = False # Set to true the frame the button is finally 'pressed'

        self.render() # Generate surfaces

    def setPos(self, x: int = None, y: int = None) -> None:

        """
        Change the button position
        :param x: New x-position, unchanged if not specified
        :param y: New y-position, unchanged if not specified
        """

        if not (x is None):
            self.pos = (x, self.pos[1])

        if not (y is None):
            self.pos = (self.pos[0], y)

    def getStyle(self, name: str) -> typing.Any:

        """
        Used to get information about the style of the object, or returns the default if it wasn't specified

        :param name: Style parameter to look up
        :return: Style used, if supplied, otherwise the default value
        """

        global buttonDefaults

        if name in self.style: # If user specified the style parameter
            return self.style[name]

        return buttonDefaults[name] # If not specified, return the default from the above definition

    def render(self) -> None:

        """
        Renders all necessary surfaces for the different button states.
        """

        global allThemes

        font: pygame.Font = pygame.font.SysFont(self.getStyle("font"), self.getStyle("size"))
        label: pygame.Surface = font.render(self.text, True, allThemes[self.theme][0]) # Generate text

        # Button size is text bounding-box size, plus some padding
        self.width = label.get_width() + self.getStyle("padding-width")
        self.height = label.get_height() + self.getStyle("padding-height")

        # Generate surfaces for the different states, and fill with the different theme colours
        self.surfaces["normal"] = pygame.Surface((self.width, self.height))
        self.surfaces["normal"].fill(allThemes[self.theme][1])

        self.surfaces["hover"] = pygame.Surface((self.width, self.height))
        self.surfaces["hover"].fill(allThemes[self.theme][2])

        self.surfaces["clicked"] = pygame.Surface((self.width, self.height))
        self.surfaces["clicked"].fill(allThemes[self.theme][3])

        # Draw rest of label
        for s in self.surfaces:

            # Add text
            self.surfaces[s].blit(label, (self.getStyle("padding-width") // 2, self.getStyle("padding-height") // 2))

            # Optional border if specified
            if self.getStyle("border"):
                pygame.draw.rect(self.surfaces[s], allThemes[self.theme][0], (0, 0, self.width, self.height), self.getStyle("border-width"))

    def draw(self, drawSurface: pygame.Surface) -> None:

        """
        Draws the button on a given surface.

        :param drawSurface: Surface to draw button on.
        """

        drawSurface.blit(self.surfaces[self.state], self.pos)  # Draw surface based on current state

    def update(self) -> None:

        """
        Updates the button's clicking logic.
        """

        self.isPressed = False # Reset value each time, so it is only true for one frame

        if local_mtouch(self.pos[0], self.pos[1], self.width, self.height): # Mouse hovering over

            # If in state 'clicked', mouse has been pressed down. Now need to wait for mouse to be released.
            if self.state == "clicked" and not local_mp:
                if not (self.function is None):
                    self.function() # Call specified function if one was given

                self.isPressed = True
                self.state = "normal"

            if self.state == "normal": # If mouse hasn't been pressed down yet, and mouse hovers over.
                self.state = "hover"

        else:

            if self.state == "hover" or self.state == "clicked": # Reset state if mouse ever leaves the button
                self.state = "normal"

        if self.state == "hover" and local_m_down: # If hovering over, and mouse just pressed down
            self.state = "clicked"

    def updateDraw(self, drawSurface: pygame.Surface) -> None:

        """
        Updates and draws the button using a single function call.
        This allows the update() and draw() functions to be used separately if needed, but can just process the entire thing using updateDraw().

        :param drawSurface: Surface to draw button on.
        """

        self.update()
        self.draw(drawSurface)

class buttonList:

    """
    A class for a row of multiple buttons.
    Can pass regular button style parameters into it, as well as some additional ones.
    Can set toggle=True to create a selector, where at any point in time exactly one button in the list will be selected.
    """

    def __init__(self, texts: typing.List[str], theme: str, pos: typing.Tuple[int, int], style: dict = None, toggle = False, onChange: typing.Callable = None) -> None:

        """
        Creates buttonList class.

        :param texts: List of button text values.
        :param theme: Colour theme to use, key from allThemes dictionary.
        :param pos: Coordinate of top-left corner of button.
        :param style: A dictionary of customisable style parameters.
        :param toggle: Set to true to create a selector, where one button in the list can be highlighted at once.
        :param onChange: Function to call when in toggle mode and a different button is clicked.
        """

        self.texts: typing.List[str] = texts
        self.theme: str = theme
        self.pos: typing.Tuple[int, int] = pos

        if not self.theme in allThemes:
            warnings.warn(f"{self.theme} theme does not exist! Defaulting to basic theme.")
            self.theme = "basic"

        if style is None:
            self.style: dict = {}
        else:
            self.style: dict = style

        self.width: int = 0
        self.height: int = 0

        self.buttons: typing.List[button] = [] # List of all individual button objects
        x = self.pos[0] # First button is at specified coordinate
        for text in self.texts:

            b = button(text, self.theme, (x, self.pos[1]), style=self.style) # Create button
            x += b.width + self.getStyle("spacing") # Increment x by last button width so that new button doesn't overlap
            self.buttons.append(b)

        # Used in toggle mode
        self.toggle = toggle
        self.selected = 0 # Currently selected button from self.buttons list
        self.onChange: typing.Callable = onChange

    def getStyle(self, name: str) -> typing.Any:

        """
        Used to get information about the style of the object, or returns the default if it wasn't specified

        :param name: Style parameter to look up
        :return: Style used, if supplied, otherwise the default value
        """

        global buttonListDefaults

        if name in self.style: # If user specified the style parameter
            return self.style[name]

        return buttonListDefaults[name] # If not specified, return the default from the above definition

    def update(self, drawSurface: pygame.Surface) -> None:

        """
        Updates the selection logic, and draws all buttons.

        :param drawSurface: Surface to draw buttons on.
        """

        for i, b in enumerate(self.buttons):
            b.update()

            if self.toggle:
                if b.isPressed: # This button was clicked
                    if self.selected != i: # Different to currently selected
                        self.selected = i # Set this as selected
                        if not self.onChange is None:
                            self.onChange() # Run supplied function

            else: # If not in toggle mode
                b.draw(drawSurface) # Can draw button straight away, no addition logic needed

        if self.toggle:
            for i, b in enumerate(self.buttons):

                    if self.selected == i: # Selected button always has "clicked" appearance, even if not actually clicked
                        b.state = "clicked" # Force state to "clicked"
                        b.draw(drawSurface) # Draw in this state
                        b.state = "normal" # Revert state to "normal" for future updates

                    else: # Not the selected option

                        clicking = False
                        if b.state == "clicked":
                            b.state = "normal" # Force button to "normal" state for drawing purposes
                            clicking = True # Need to remember if the user is pressing the mouse on the button

                        b.draw(drawSurface) # Draw in the "normal" state

                        if clicking:
                            b.state = "clicked" # Revert back to "clicked" state for future updates if the user is clicking on the button
