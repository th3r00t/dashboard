import configparser
from dataclasses import dataclass
from typing import List, Any
from pathlib import Path

@dataclass
class Config:
    mem: List
    cpu: List
    parser: configparser.ConfigParser
    obj: Any
    path: Path

    def __init__(self):
        config_dir = Path.home()/".config"/"dashboard"
        config_file = config_dir/"config.ini"
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
            self.make_initial_config(config_file)
        self.parser = configparser.ConfigParser()
        self.file = config_file 
        self.settings = self.load()

    def load(self):
        return self.parser.read(self.file) 

    def make_initial_config(self, path):
        parser = configparser.ConfigParser()
        parser['Settings'] = {'wx_loc': 'Paris'}
        with open(path, 'w') as file:
            parser.write(file)
