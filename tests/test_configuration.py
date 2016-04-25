"""
Unit tests for the configuration loader module.
"""
import os
import json

from pycraft.configuration import ConfigurationLoader


DEFAULT_CONFIG = {
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
    },
}


def test_config_init():
    """
    Test that the ConfigurationLoader object is generated correctly and returns
    a config dictionary as expected.
    """
    config = ConfigurationLoader()
    # check an object was created
    assert config, "No ConfigurationLoader object created!"

    # Get the config and check it is the default values
    config_dict = config.get_configurations()
    assert config_dict == DEFAULT_CONFIG, "Config created didn't match default config"


def test_load_configuration_file():
    """
    Test that we can read and write a config file.
    """
    config = ConfigurationLoader()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'tmp-configuration.json')
    config.configuration_file_path = config_path

    # There shouldn't be a config file, so it will write one
    config_dict = config.load_configuration_file()
    assert os.path.exists(config_path), "Didn't write a config file!"
    assert config_dict == DEFAULT_CONFIG, "Config returned doesn't match default config"
    with open(config_path, 'r') as f:
        written_config = json.load(f)
    assert written_config == DEFAULT_CONFIG, "Written config doesn't match default config"

    # Now we want to do it all again writing our own config file
    new_config = {
        "window": {
            "width": 813,
            "height": 2450,
            "ticks_per_second": 63,
            "resizeable": False,
            "exclusive_mouse": False,
        },
        "controls": {
            "forward": "Z",
            "backward": "S",
            "right": "D",
            "left": "Q",
            "jump": "LSHIFT",
            "down": "TAB",
            "fly": "SPACE",
        },
        "world": {
            "gravity": 234.0,
            "player_height": 123,
            "max_jump_height": 34.1,
            "terminal_velocity": 431,
            "walking_speed": 12,
            "flying_speed": 34,
        },
    }

    with open(config_path, 'w') as f:
        json.dump(new_config, f, indent=4)
    opened_config = config.load_configuration_file()
    assert opened_config == new_config, "Loaded config doesn't match what we wrote"

    # Clean up after ourselves
    os.remove(config_path)


if __name__ == "__main__":
    test_config_init()
    test_load_configuration_file()
