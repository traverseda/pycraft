import time
from collections import OrderedDict

from noise.perlin import SimplexNoise
from pyglet import image
from pyglet.gl import glClearColor, glEnable, GL_CULL_FACE, glTexParameteri, \
    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST, \
    GL_TEXTURE_MAG_FILTER, GL_FOG, glFogfv, GL_FOG_COLOR, \
    GLfloat, glHint, GL_FOG_HINT, GL_DONT_CARE, glFogi, \
    GL_FOG_MODE, GL_LINEAR, glFogf, GL_FOG_START, \
    GL_FOG_END, GL_QUADS
from pyglet.graphics import Batch, TextureGroup

from pycraft.objects import Brick, Grass, Sand, Stone
from pycraft.util import normalize, sectorize, reverse_sectorize, \
    cube_vertices, cube_shade
from pycraft.shader import Shader

simplex_noise2 = SimplexNoise(256).noise2

FACES = [
    (0, 1, 0),
    (0, -1, 0),
    (-1, 0, 0),
    (1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
]


class World:
    def __init__(self):
        # A Batch is a collection of vertex lists for batched rendering.
        self.batch = Batch()
        # A TextureGroup manages an OpenGL texture.
        self.texture_group = {}
        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the world.
        self.objects = {}
        # Same mapping as `world` but only contains blocks that are shown.
        self.shown = {}
        # Mapping from position to a pyglet `VertextList` for all shown blocks.
        self._shown = {}
        # Which sector the player is currently in.
        self.sector = None
        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}

        self.shader = None
        self.show_hide_queue = OrderedDict()
        self.init_gl()
        self.init_shader()

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

    def hit_test(self, position, vector, max_distance=8):
        """Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.
        """
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.objects:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    def exposed(self, position):
        """Returns False is given `position` is surrounded on all 6 sides by
        blocks, True otherwise.
        """
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.objects:
                return True
        return False

    def add_block(self, position, texture, immediate=True):
        """Add a block with the given `texture` and `position` to the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to add.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.
        immediate : bool
            Whether or not to draw the block immediately.
        """
        if position in self.objects:
            self.remove_block(position, immediate)
        self.objects[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)

    def remove_block(self, position, immediate=True):
        """Remove the block at the given `position`.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to remove.
        immediate : bool
            Whether or not to immediately remove block from canvas.
        """
        del self.objects[position]
        self.sectors[sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)

    def check_neighbors(self, position):
        """Check all blocks surrounding `position` and ensure their visual
        state is current. This means hiding blocks that are not exposed and
        ensuring that all exposed blocks are shown. Usually used after a block
        is added or removed.
        """
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.objects:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)

    def show_block(self, position, immediate=True):
        """Show the block at the given `position`. This method assumes the
        block has already been added with add_block()

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        immediate : bool
            Whether or not to show the block immediately.
        """
        texture = self.objects[position]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self.show_hide_queue[position] = True

    def _show_block(self, position, block):
        """Private implementation of the `show_block()` method.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.
        """
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        shade_data = cube_shade(1, 1, 1, 1)
        texture_data = block.texture
        if block.identifier not in self.texture_group:
            self.texture_group[block.identifier] = TextureGroup(image.load(block.texture_path).get_texture())
        self._shown[position] = self.batch.add(
            24, GL_QUADS, self.texture_group[block.identifier],
            ('v3f/static', vertex_data),
            ('c3f/static', shade_data),
            ('t2f/static', texture_data))

    def hide_block(self, position, immediate=True):
        """Hide the block at the given `position`. Hiding does not remove the
        block from the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to hide.
        immediate : bool
            Whether or not to immediately remove the block from the canvas.
        """
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self.show_hide_queue[position] = False

    def _hide_block(self, position):
        """Private implementation of the 'hide_block()` method."""
        self._shown.pop(position).delete()

    def show_sector(self, sector):
        """Ensure all blocks in the given sector that should be shown are drawn
        to the canvas.
        """
        positions = self.sectors.get(sector, [])
        if positions:
            for position in positions:
                if position not in self.shown and self.exposed(position):
                    self.show_block(position, False)
        else:
            self.generate_sector(sector)
            self.show_sector(sector)

    def generate_sector(self, sector):
        """Generate blocks within sector using simplex_noise2
        """
        for column in reverse_sectorize(sector):
            x, z = column
            y_max = int((simplex_noise2(x / 30, z / 30) + 1) * 3)
            for y_lvl in range(0 - 2, y_max):
                self.add_block((x, y_lvl, z), Sand(), immediate=False)
            else:
                self.add_block((x, y_lvl, z), Grass(), immediate=False)
            # add the safety stone floor.
            # don't want anyone falling into the ether.
            self.add_block((x, 0 - 3, z), Stone(), immediate=False)

    def hide_sector(self, sector):
        """Ensure all blocks in the given sector that should be hidden are
        removed from the canvas.
        """
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

    def change_sectors(self, before, after):
        """Move from sector `before` to sector `after`. A sector is a
        contiguous x, y sub-region of world. Sectors are used to speed up
        world rendering.
        """
        before_set = set()
        after_set = set()
        pad = 4
        for dx in range(-pad, pad + 1):
            for dy in [0]:  # range(-pad, pad + 1):
                for dz in range(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)

    def _dequeue(self):
        """Pop the top function from the internal queue and call it."""
        position, show = self.show_hide_queue.popitem(last=False)
        shown = position in self._shown
        if show and not shown:
            self._show_block(position, self.objects[position])
        elif shown and not show:
            self._hide_block(position)

    def process_queue(self, ticks_per_sec):
        """Process the entire queue while taking periodic breaks. This allows
        the game loop to run smoothly. The queue contains calls to
        _show_block() and _hide_block() so this method should be called if
        add_block() or remove_block() was called with immediate=False
        """
        start = time.clock()
        while self.show_hide_queue and time.clock() - start < 1.0 / ticks_per_sec:
            self._dequeue()

    def process_entire_queue(self):
        """Process the entire queue with no breaks."""
        while self.show_hide_queue:
            self._dequeue()

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
