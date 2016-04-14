import pyglet.app

from pycraft.window import Window
from pycraft.world import World
from pycraft.player import Player

WINDOW_DIMENSIONS = (800, 600)
WINDOW_CAPTION = 'PyCraft'
WINDOW_RESIZEABLE = True
WINDOW_EXCLUSIVE_MOUSE = True

def main():
    window = Window(
        width=WINDOW_DIMENSIONS[0],
        height=WINDOW_DIMENSIONS[1],
        caption=WINDOW_CAPTION,
        resizable=WINDOW_RESIZEABLE
    )
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse(WINDOW_EXCLUSIVE_MOUSE)
    world = World()
    window.set_world(world)
    player = Player()
    window.set_player(player)
    pyglet.app.run()
