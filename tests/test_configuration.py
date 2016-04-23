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
    config_path = config.configuration_file_path

    # Check that there isn't already a config file at this location,
    # we don't want to overwrite user data!
    if os.path.exists(config_path):
        os.rename(config_path, config_path + ".backup")

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
            "width": 800,
            "height": 600,
            "ticks_per_second": 60,
            "resizeable": True,
            "exclusive_mouse": True,
        },
        "controls": {
            "forward": "Z",
            "backward": "S",
            "right": "D",
            "left": "Q",
            "jump": "SPACE",
            "down": "LSHIFT",
            "fly": "TAB",
        },
    }
    with open(config_path, 'w') as f:
        json.dump(new_config, f)
    opened_config = config.load_configuration_file()
    assert opened_config == new_config, "Loaded config doesn't match what we wrote"

    # Clean up after ourselves
    if os.path.exists(config_path + ".backup"):
        os.rename(config_path + ".backup", config_path)
    else:
        os.remove(config_path)


if __name__ == "__main__":
    test_config_init()
    test_load_configuration_file()
