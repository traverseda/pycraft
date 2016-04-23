"""
    Requires python version 3.4 or greater
"""
from enum import Enum


class States(Enum):
    MAIN_SCREEN = 1
    MAIN_MENU = 2
    RUNNING = 3
    INVENTORY_MENU = 4
    CRAFTING_MENU = 5
    OPTIONS_MENU = 6


"""
    Just an interface. All Game States implementation defined in the States
    enum should extend this class and implement those methods
"""


class GameState:

    def __init__(self):
        pass

    """
        Think about those resposabilities from the GameState.
        Some game states may only need to be updated, while another only need
        to be drawn
    """

    def on_update(self):
        pass

    def on_draw(self):
        pass

    """
        Are those responsibilities of the Game State class?
    """

    def on_input(self):
        pass

    def on_click(self):
        pass

    # --- ** ---
    # Methods related to the GameStateManager
    """
        To be called AFTER the game state has been placed in the
        GameStateManager stack
    """

    def on_entered(self):
        pass

    """
        To be called BEFORE the game state is removed from the game
        state manager
    """

    def on_leaving(self):
        pass

    """
        To be called BEFORE another game state is stacked on top of the actual
    """

    def on_obscuring(self):
        pass

    """
        To be called AFTER this actual game state to be on the top of the
        GameStateManager stacked
    """

    def on_revealed(self):
        pass

"""
    Desirable option for game states switch - don't let this function for the
    main method

    It's implemented as a stack in order to let game states return to previous
    one without  the need it to know for which state it is returning to (e.g.
    maps and option menus)
"""


class GameStateManager:

    def __init__(self):
        self.stack = list()

    # TODO define a good way to map each possible game state
    def switch_game_state(self):
        pass

    def peek(self):
        return self.stack[len(self.stack) - 1]

    def pop(self):
        return self.stack.pop()

    def push(self, game_state):
        self.stack.append(game_state)
