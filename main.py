import utilities, gui
import pygame
from pygame.locals import *
import numpy
import PIL
import typing

# ----- Pygame Setup -----

clock = pygame.time.Clock()
pygame.init()

displayInfo = pygame.display.Info()
screen = pygame.display.set_mode((displayInfo.current_w - 50, displayInfo.current_h - 100), RESIZABLE)
screenSize: typing.Tuple[int, int] = screen.get_size()

backcolour: typing.Tuple[int, int, int]  = (100, 100, 100)

mx: int = 0 # Current mouse x-position
my: int = 0 # Current mouse y-position
mp: bool = False # If LMB down
mp2: bool = False # If RMB down
m_down: bool = False # Set to true on the single frame LMB pressed, false otherwise
keys = [] # Keys currently being pressed

pygame.display.set_caption("Video Editor")

def txt(size: int, text: str, color: typing.Tuple[int, int, int], tx: int, ty: int) -> None:

    """
    Renders text on screen. Not particularly efficient method, better to pre-render.
    :param size: Text size
    :param text: String to render
    :param color: RGB tuple
    :param tx: x-position to render
    :param ty: y-position to render
    """

    font = pygame.font.SysFont('arial', size) # Get system font
    label = font.render(text, 1, color) # Render text
    screen.blit(label, (tx, ty)) # Draw on main surface

def mtouch(tx: int, ty: int, tw: int, th: int) -> bool:

    """
    Detects if the mouse is touching a defined rectangular region.
    :param tx: x-position of top-left corner of detection region
    :param ty: y-position of top-left corner
    :param tw: Width of region
    :param th: Height of region
    :return: True if mouse is within region
    """

    t = False
    if tx < mx < tx + tw:
        if ty < my < ty + th:
            t = True
    return t

# ----- Setup -----
b = gui.button("Test", "dark", (10, 10), style={"border":True, "border-width": 1}) # Example button

# ----- Main loop -----

running = True
while running:

    screen.fill(backcolour)

    # updates variables
    mx = pygame.mouse.get_pos()[0]
    my = pygame.mouse.get_pos()[1]
    mp = pygame.mouse.get_pressed()[0]
    mp2 = pygame.mouse.get_pressed()[2]
    keys = pygame.key.get_pressed()

    clock.tick(60)
    fps = int(clock.get_fps())

    pygame.display.set_caption(f"Video Editor | FPS: {fps}")

    m_down = False # Reset value
    for event in pygame.event.get():

        if event.type == pygame.QUIT: # Cross button clicked
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # LMB pressed
                m_down = True # Set to true for one loop

        elif event.type == pygame.VIDEORESIZE: # User resized the window
            screenSize = screen.get_size() # Update with the new size

    # ----------

    gui.updateLocals(mx, my, mp, m_down) # Pass mouse data to gui library
    b.update(screen) # Draw and update button

    pygame.display.flip()

pygame.quit()
