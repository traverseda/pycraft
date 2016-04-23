"""
Unit tests for the util.py module.
"""
import pycraft.util as util


def test_cube_vertices():
    """
    Test cube_vertices function.
    """
    vertices = util.cube_vertices(0, 10, 20, 0.5)

    # 6 groups of each 12 numbers. those numbers are 4 3-tuple coordinates
    # making up the 6 sides of a cube
    groups = [vertices[i:i + 12] for i in range(0, 72, 12)]
    total_coords = set()
    for i, group in enumerate(groups):
        coords = [tuple(group[j:j + 3]) for j in range(0, 12, 3)]
        total_coords |= set(coords)
        assert len(coords) == len(set(coords)), 'Face coords not unique'
        if i in (0, 1):
            # top/bottom: y should always be the same
            assert len(set(c[1] for c in coords)) == 1
        elif i in (2, 3):
            # left/right, x should always be the same
            assert len(set(c[0] for c in coords)) == 1
        elif i in (4, 5):
            # front/back, z should always be the same
            assert len(set(c[2] for c in coords)) == 1
    assert len(total_coords) == 8, 'A cube has exactly 8 corners'


def test_normalize():
    """
    Test the normalize function.
    """
    my_pos = [3.29, 5.9, 7.001]
    expected = [3, 6, 7]
    norm_pos = util.normalize(my_pos)
    for i, e in zip(norm_pos, expected):
        assert isinstance(i, int), "Returned position not an integer"
        assert i == e, "Returned postion ({}) not what we expected ({})!".format(i, e)


def test_sectorize():
    """
    Test the sectorize function.
    Currently assumes sector_size is 16, should make this not hard coded!
    """
    my_pos = [65, 30, 65]
    expected = [4, 0, 4]
    sector = util.sectorize(my_pos)
    for i, e in zip(sector, expected):
        assert i == e, "Returned sector not what was expected"


if __name__ == "__main__":
    test_cube_vertices()
    test_normalize()
    test_sectorize()
