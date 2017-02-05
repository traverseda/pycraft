from pyglet.gl import glClearColor, glEnable, GL_CULL_FACE, glTexParameteri, \
    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST, \
    GL_TEXTURE_MAG_FILTER, GL_FOG, glFogfv, GL_FOG_COLOR, \
    GLfloat, glHint, GL_FOG_HINT, GL_DONT_CARE, glFogi, \
    GL_FOG_MODE, GL_LINEAR, glFogf, GL_FOG_START, \
    GL_FOG_END


class PycraftOpenGL:
    def __init__(self):
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
