import pyglet.app

from pycraft.window import Window
from pycraft.world import World
from pycraft.objects.player import Player
from pycraft.configuration import ConfigurationLoader

WINDOW_CAPTION = 'PyCraft'


def main():
    # Load configuration file
    config_loader = ConfigurationLoader()
    config_data = config_loader.load_configuration_file()
    config_loader.check_configuration()

    window = Window(
        ticks_ps=config_data["window"]["ticks_per_second"],
        width=config_data["window"]["width"],
        height=config_data["window"]["height"],
        caption=WINDOW_CAPTION,
        resizable=config_data["window"]["resizeable"]
    )
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse(config_data["window"]["exclusive_mouse"])
    # world = World()
    # window.set_world(world)
    # player = Player(config_data["world"])
    # window.set_player(player)
    pyglet.app.run()
