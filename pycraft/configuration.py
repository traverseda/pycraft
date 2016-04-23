from os.path import expanduser
import sys
import json

'''
    The configuration file will be stored as a json file

    @example
    {
        window: {
            w_dimension:     800
            h_dimension:     600
            resizeable:        False
        }
    }
'''


class ConfigurationLoader:
    '''

    '''

    def __init__(self):
        '''
                Initialize with defaut values
        '''
        self.game_config = dict()
        self.game_config["window"] = dict()
        self.game_config["window"]["width"] = 800
        self.game_config["window"]["height"] = 600
        self.game_config["window"]["ticks_per_second"] = 60
        self.game_config["window"]["resizeable"] = True
        self.game_config["window"]["exclusive_mouse"] = True

        # Prepare acess to the configuration file
        home_directory = expanduser("~")
        self.configuration_file_path = home_directory + "/.pycraftconfig.json"

    def load_configuration_file(self):

        try:
            json_data = json.load(open(self.configuration_file_path))

            try:
                self.game_config["window"][
                    "width"] = json_data["window"]["width"]
                self.game_config["window"][
                    "height"] = json_data["window"]["height"]
                self.game_config["window"]["ticks_per_second"] = json_data[
                    "window"]["ticks_per_second"]
                self.game_config["window"][
                    "resizeable"] = json_data["window"]["resizeable"]
                self.game_config["window"]["exclusive_mouse"] = json_data[
                    "window"]["exclusive_mouse"]
            except KeyError:
                # Think about display informations in the screen
                sys.exit("Exiting! Configuration file format error!")

        except IOError:
            # Create a new configuration file with the defaut values stored in
            # the config_game variable
            with open(self.configuration_file_path, 'w') as f:
                json.dump(self.game_config, f)

        return self.game_config

    def get_configurations(self):
        return self.game_config
