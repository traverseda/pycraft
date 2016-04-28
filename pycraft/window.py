# 3rd party imports
import pyglet.clock
import pyglet.window
from pyglet.window import key, mouse

from pycraft.configuration import ConfigurationLoader
from pycraft.gamestate import GameStateManager, States
from pycraft.gs_running import GameStateRunning


class Window(pyglet.window.Window):
    def __init__(self, ticks_ps, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.ticks_per_second = ticks_ps
        # Whether or not the window exclusively captures the mouse.
        self.set_exclusive_mouse(False)
        # This call schedules the `update()` method to be called
        # ticks_per_second. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / self.ticks_per_second)
        config_loader = ConfigurationLoader()
        self.config_data = config_loader.load_configuration_file()

        # Create the game state manager and set the first state
        self.gamestatemanager = GameStateManager()
        # This should be changed when we implement the MAINMENU game state
        gs_running = GameStateRunning(self.config_data, height=self.height, width=self.width)
        self.gamestatemanager.push(gs_running)

    def set_exclusive_mouse(self, exclusive):
        """If `exclusive` is True, the game will capture the mouse, if False the
        game will ignore the mouse.
        """
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def on_mouse_press(self, x, y, button, modifiers):
        """Called when a mouse button is pressed. See pyglet docs for button
        amd modifier mappings.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        button : int
            Number representing mouse button that was clicked. 1 = left button,
            4 = right button.
        modifiers : int
            Number representing any modifying keys that were pressed when the
            mouse button was clicked.
        """

        if self.exclusive:
            self.gamestatemanager.peek().on_mouse_press(x, y, button, modifiers)
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the player moves the mouse.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        dx, dy : float
            The movement of the mouse.
        """
        if self.exclusive:
            self.gamestatemanager.peek().on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        """Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.
        config_data["controls"] : dict
            control map read by the configuration file
        """
        if symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        else:
            self.gamestatemanager.peek().on_key_press(symbol, modifiers, self.config_data["controls"])

    def on_key_release(self, symbol, modifiers):
        """Called when the player releases a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.
        config_data["controls"] : dict
            control map read by the configuration file
        """
        self.gamestatemanager.peek().on_key_release(symbol, modifiers, self.config_data["controls"])

    def on_resize(self, width, height):
        """Called when the window is resized to a new `width` and `height`."""
        self.gamestatemanager.peek().on_resize(width, height)

    def on_draw(self):
        """Called by pyglet to draw the canvas.

            Pass the current window size
        """
        self.clear()
        self.gamestatemanager.peek().on_draw(self.get_size())

    def update(self, dt):
        """This method is scheduled to be called repeatedly by the pyglet
        clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.
        ticks_per_second:
        """
        self.gamestatemanager.peek().update(dt, self.ticks_per_second)
