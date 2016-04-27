# python imports
import math

# project imports
from .object import WorldObject
from ..util import normalize

FACES = [
    (0, 1, 0),
    (0, -1, 0),
    (-1, 0, 0),
    (1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
]


class Character(WorldObject):
    """
        Class to abstract common logic between players and npc characters
    """
    def __init__(self, config):
        # general world configuration
        self.config = config
        # To derive the formula for calculating jump speed, first solve
        #    v_t = v_0 + a * t
        # for the time at which you achieve maximum height, where a is the acceleration
        # due to gravity and v_t = 0. This gives:
        #    t = - v_0 / a
        # Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
        #    s = s_0 + v_0 * t + (a * t^2) / 2
        self.jump_speed = math.sqrt(2 * self.config['gravity'] * self.config['max_jump_height'])
        # When flying gravity has no effect and speed is increased.
        self.flying = False
        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.strafe = [0, 0]
        # This is strafing in the absolute up/down position, not
        # relative to where the player is facing. 1 when moving up, -1 when moving down
        self.strafe_z = 0
        # Current (x, y, z) position in the world, specified with floats. Note
        # that, perhaps unlike in math class, the y-axis is the vertical axis.
        self.position = (0, 5, 0)
        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)
        # Velocity in the y (upward) direction.
        self.dy = 0

    def strafe_forward(self):
        self.strafe[0] -= 1

    def strafe_backward(self):
        self.strafe[0] += 1

    def strafe_right(self):
        self.strafe[1] += 1

    def strafe_left(self):
        self.strafe[1] -= 1

    def strafe_up(self):
        if self.flying:
            self.strafe_z += 1

    def strafe_down(self):
        if self.flying:
            self.strafe_z -= 1

    def jump(self):
        """Increases vertical velocity, if grounded. If flying, moves upwards"""
        if self.flying:
            self.strafe_up()
        else:
            if self.dy == 0:
                self.dy = self.jump_speed

    def fly(self):
        """Toggles flying mode"""
        self.flying = not self.flying
        self.strafe_z = 0

    def get_motion_vector(self):
        """Returns the current motion vector indicating the velocity of the player.

        Returns
        -------
        vector : tuple of len 3
            Tuple containing the velocity in x, y, and z respectively.
        """
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    # Moving left or right.
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # Moving backwards.
                    dy *= -1
                # When you are flying up or down, you have less left and right motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        dy += self.strafe_z
        return dx, dy, dz

    def update(self, dt, objects):
        """Private implementation of the `update()` method. This is where most
        of the motion logic lives, along with gravity and collision detection.

        Parameters
        ----------
        dt : float
            The change in time since the last call.
        objects: list of blocks
        """
        speed = self.config['flying_speed'] if self.flying else self.config['walking_speed']
        d = dt * speed  # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.dy -= dt * self.config['gravity']
            self.dy = max(self.dy, -self.config["terminal_velocity"])
            dy += self.dy * dt
        # collisions
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), self.config["player_height"], objects)
        self.position = (x, y, z)

    def collide(self, position, height, objects):
        """Checks if the character at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.
        objects: list of blocks

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.
        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall grass. If >= .5, you'll fall through the ground.
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:  # check all surrounding blocks
            for i in range(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in range(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in objects:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        self.dy = 0
                    break
        return tuple(p)
