from os.path import expanduser
import sys
import json
import collections
from pyglet.window import key


"""
    The configuration file will be stored as a json file

    @example
    {
        window: {
            w_dimension:     800
            h_dimension:     600
            resizeable:        False
        }
    }
"""


def update_dict(d, u):
    for key_, value in u.items():
        if isinstance(value, collections.Mapping):
            r = update_dict(d.get(key_, {}), value)
            d[key_] = r
        else:
            d[key_] = u[key_]
    return d


class ConfigurationLoader:
    """

    """

    def __init__(self):
        """
            Initialize with defaut values
        """
        self.game_config = {
            "window": {
                "width": 800,
                "height": 600,
                "ticks_per_second": 60,
                "resizeable": True,
                "exclusive_mouse": True,
            },
            "controls": {
                "forward": "W",
                "backward": "S",
                "right": "D",
                "left": "A",
                "jump": "SPACE",
                "down": "LSHIFT",
                "fly": "TAB",
            },
            "world": {
                "gravity": 20.0,
                "player_height": 2,
                "max_jump_height": 2.0,
                "terminal_velocity": 50,
                "walking_speed": 5,
                "flying_speed": 15,
            }
        }

        # Prepare acess to the configuration file
        home_directory = expanduser("~")
        self.configuration_file_path = home_directory + "/.pycraftconfig.json"

    def load_configuration_file(self):
        try:
            json_data = json.load(open(self.configuration_file_path))
            update_dict(self.game_config, json_data)
        except IOError:
            # Create a new configuration file with the defaut values stored
            # in the config_game variable
            with open(self.configuration_file_path, 'w') as f:
                json.dump(self.game_config, f)

        return self.game_config

    def get_configurations(self):
        return self.game_config

    def check_configuration(self):
        for k, v in self.game_config['controls'].items():
            print(k, v)
            try:
                getattr(key, v)
            except AttributeError:
                sys.exit("The key configration for '%s' is wrong" % k)
