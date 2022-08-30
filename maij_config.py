import json
import os
from json import JSONEncoder

from .const import *

key_group_location = 'group_location'


class Config:
    group_location = dict()

    def __init__(self):
        # if config.json doesn't exist, create directories and file
        if not os.path.exists(CONFIG_PATH):
            if not os.path.exists(CONFIG_DIR):
                os.makedirs(CONFIG_DIR)
            with open(CONFIG_PATH, 'w') as config_file:
                config_json = {key_group_location: {}}
                json.dump(config_json, config_file)
        self.load()

    def load(self):
        with open(CONFIG_PATH, 'r') as config_file:
            # load config.json from disk
            config_data = json.load(config_file)
            # initialize group_location
            self.group_location = dict()
            for group_id, locate in config_data[key_group_location].items():
                self.group_location[int(group_id)] = locate

    def write_to_disk(self):
        with open(CONFIG_PATH, 'w') as config_file:
            json.dump(self, config_file, cls=ConfigEncoder, ensure_ascii=False)


class ConfigEncoder(JSONEncoder):
    def default(self, o: Config):
        return o.__dict__


plugin_config = Config()
