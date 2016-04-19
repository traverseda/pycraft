import pytest
import mock

from pycraft.objects.player import Player, JUMP_SPEED
from pycraft.objects.block import Brick, Grass, Sand

@pytest.fixture
def player():
    return Player()

def test_strafes_forward(player):
    player.strafe_forward()
    assert player.strafe == [-1, 0]

def test_strafes_backward(player):
    player.strafe_backward()
    assert player.strafe == [1, 0]

def test_strafes_left(player):
    player.strafe_left()
    assert player.strafe == [0, -1]

def test_strafes_right(player):
    player.strafe_right()
    assert player.strafe == [0, 1]

def test_no_initial_dy(player):
    assert player.dy == 0

def test_jumps(player):
    player.jump()
    assert player.dy == JUMP_SPEED

def test_not_flying_initially(player):
    assert player.flying == False

def test_flies(player):
    player.fly()
    assert player.flying == True

def test_brick_selected_by_default(player):
    assert isinstance(player.block, Brick)

def test_switches_inventory(player):
    expected = [Brick, Grass, Sand, Brick]
    for i in range(0, len(expected)):
        player.switch_inventory(i)
        assert isinstance(player.block, expected[i])
