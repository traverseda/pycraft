# Size of sectors used to ease block loading.
SECTOR_SIZE = 16


def cube_vertices(x, y, z, n):
    """Return the vertices of the cube at position x, y, z with size 2*n."""
    return [
        x - n, y + n, z - n, x - n, y + n, z + n, x +
        n, y + n, z + n, x + n, y + n, z - n,  # top
        x - n, y - n, z - n, x + n, y - n, z - n, x + \
        n, y - n, z + n, x - n, y - n, z + n,  # bottom
        x - n, y - n, z - n, x - n, y - n, z + n, x - \
        n, y + n, z + n, x - n, y + n, z - n,  # left
        x + n, y - n, z + n, x + n, y - n, z - n, x + \
        n, y + n, z - n, x + n, y + n, z + n,  # right
        x - n, y - n, z + n, x + n, y - n, z + n, x + \
        n, y + n, z + n, x - n, y + n, z + n,  # front
        x + n, y - n, z - n, x - n, y - n, z - n, x - \
        n, y + n, z - n, x + n, y + n, z - n,  # back
    ]


def cube_shade(x, y, z, n):
    """Return the color diference between the sides of the cube."""
    return [
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  # top
        0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,  # bottom
        0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,  # left
        0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8,  # right
        0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,  # front
        0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8,  # back
    ]


def normalize(position):
    """Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3
    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return x, y, z


def sectorize(position):
    """Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    sector : tuple of len 3
    """
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return x, 0, z

def reverse_sectorize(sector):
    """Returns an array of positions that would be found in a given sector.
    Parameters
    ----------
    sector: tuple of len 3
    Returns
    -------
    columns: tuple of len SECTOR_SIZE**2; containing tuples of len 2
    """
    columns  = []
    sector_x,sector_z,sector_z = sector
    x_start,z_start = sector_x*SECTOR_SIZE, sector_z*SECTOR_SIZE
    x_end,z_end = x_start+SECTOR_SIZE, z_start+SECTOR_SIZE
    for x in range(x_start,x_end):
        for z in range(z_start,z_end):
            columns += [(x,z)]
    return tuple(columns)
