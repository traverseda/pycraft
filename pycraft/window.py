import math

import pyglet.clock
import pyglet.graphics
import pyglet.window
from pyglet.gl import *
from pyglet.window import key, mouse

from pycraft.objects import brick, grass, sand, stone
from pycraft.shader import Shader
from pycraft.util import sectorize, cube_vertices

TICKS_PER_SEC = 60
# Convenience list of num keys.
NUMERIC_KEYS = [
    key._1, key._2, key._3, key._4, key._5,
    key._6, key._7, key._8, key._9, key._0
]


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gl()
        self.shader = None
        self.init_shader()
        self.set_world(None)
        self.set_player(None)
        # The crosshairs at the center of the screen.
        self.reticle = None
        # The label that is displayed in the top left of the canvas.
        self.label = pyglet.text.Label(
            '', font_name='Arial', font_size=18,
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            color=(0, 0, 0, 255))
        # Whether or not the window exclusively captures the mouse.
        self.set_exclusive_mouse(False)
        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)

    def init_gl(self):
        """Basic OpenGL configuration."""
        # Set the color of "clear", i.e. the sky, in rgba.
        glClearColor(0.5, 0.69, 1.0, 1)
        # Enable culling (not rendering) of back-facing facets -- facets that aren't
        # visible to you.
        glEnable(GL_CULL_FACE)
        # Set the texture minification/magnification function to GL_NEAREST (nearest
        # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
        # "is generally faster than GL_LINEAR, but it can produce textured images
        # with sharper edges because the transition between texture elements is not
        # as smooth."
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.init_gl_fog()

    def init_gl_fog(self):
        """Configure the OpenGL fog properties."""
        # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
        # post-texturing color."
        glEnable(GL_FOG)
        # Set the fog color.
        glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
        # Say we have no preference between rendering speed and quality.
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        # Specify the equation used to compute the blending factor.
        glFogi(GL_FOG_MODE, GL_LINEAR)
        # How close and far away fog starts and ends. The closer the start and end,
        # the denser the fog in the fog range.
        glFogf(GL_FOG_START, 20.0)
        glFogf(GL_FOG_END, 60.0)

    def init_shader(self):
        vertex_shader = ""
        fragment_shader = ""

        with open("pycraft/shaders/world.vert") as handle:
            vertex_shader = handle.read()

        with open("pycraft/shaders/world.frag") as handle:
            fragment_shader = handle.read()

        self.shader = Shader([vertex_shader], [fragment_shader])

    def start_shader(self):
        self.shader.bind()

    def stop_shader(self):
        self.shader.unbind()

    def set_world(self, world):
        self.world = world

    def set_player(self, player):
        self.player = player

    def set_exclusive_mouse(self, exclusive):
        """If `exclusive` is True, the game will capture the mouse, if False the
        game will ignore the mouse.
        """
        super().set_exclusive_mouse(exclusive)
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
            vector = self.player.get_sight_vector()
            block, previous = self.world.hit_test(self.player.position, vector)
            if (button == mouse.RIGHT) or \
                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # ON OSX, control + left click = right click.
                if previous:
                    self.world.add_block(previous, self.player.block)
            elif button == pyglet.window.mouse.LEFT and block:
                texture = self.world.objects[block]
                if texture != stone:
                    self.world.remove_block(block)
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
            m = 0.15
            x, y = self.player.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.player.rotation = (x, y)

    def on_key_press(self, symbol, modifiers):
        """Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.
        """
        if symbol == key.W: self.player.strafe_forward()
        elif symbol == key.S: self.player.strafe_backward()
        elif symbol == key.D: self.player.strafe_right()
        elif symbol == key.A: self.player.strafe_left()
        elif symbol == key.SPACE: self.player.jump()
        elif symbol == key.ESCAPE: self.set_exclusive_mouse(False)
        elif symbol == key.TAB: self.player.fly()
        elif symbol in NUMERIC_KEYS:
            self.player.switch_inventory(symbol - NUMERIC_KEYS[0])

    def on_key_release(self, symbol, modifiers):
        """Called when the player releases a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.
        """
        if symbol == key.W: self.player.strafe_backward()
        elif symbol == key.S: self.player.strafe_forward()
        elif symbol == key.A: self.player.strafe_right()
        elif symbol == key.D: self.player.strafe_left()

    def on_resize(self, width, height):
        """Called when the window is resized to a new `width` and `height`."""
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def on_draw(self):
        """Called by pyglet to draw the canvas."""
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.start_shader()
        self.world.batch.draw()
        self.stop_shader()
        self.draw_focused_block()
        self.set_2d()
        self.draw_label()
        self.draw_reticle()

    def set_3d(self):
        """Configure OpenGL to draw in 3d."""
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.player.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.player.position
        glTranslatef(-x, -y, -z)

    def set_2d(self):
        """Configure OpenGL to draw in 2d."""
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def update(self, dt):
        """This method is scheduled to be called repeatedly by the pyglet
        clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.
        """
        self.world.process_queue(TICKS_PER_SEC)
        sector = sectorize(self.player.position)
        if sector != self.world.sector:
            self.world.change_sectors(self.world.sector, sector)
            if self.world.sector is None:
                self.world.process_entire_queue()
            self.world.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in range(m):
            self.player.update(dt / m, self.world.objects)

    def draw_focused_block(self):
        """Draw black edges around the block that is currently under the
        crosshairs.
        """
        vector = self.player.get_sight_vector()
        block = self.world.hit_test(self.player.position, vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        """Draw the label in the top left of the screen."""
        x, y, z = self.player.position
        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), x, y, z,
            len(self.world._shown), len(self.world.objects))
        self.label.draw()

    def draw_reticle(self):
        """Draw the crosshairs in the center of the screen."""
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)
