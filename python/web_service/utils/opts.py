import argparse
import yaml


class Config:
    def __init__(self, entries=None):
        if entries is None:
            entries = {}
        for k, v in entries.items():
            if k != 'params' and isinstance(v, dict):
                self.__dict__[k] = Config(v)
            else:
                self.__dict__[k] = v


'''
Load configuration from YAML file

Input: 
    file_path(str): 

Output:
    config(dict)
'''


def load_config(file_path):
    f = open(file_path, 'r', encoding = 'utf-8')
    config = yaml.load(f.read(), Loader = yaml.FullLoader)
    return config


def parse_opt():
    config = ""
    try:
        parser = argparse.ArgumentParser()
        # config file
        parser.add_argument(
            '--config',
            type=str,
            default='cnn1d.yaml',
            help='path to the configuration file (yaml)'
        )
        args = parser.parse_args()
        config = args.config
    except:
        config = 'cnn1d.yaml'

    config_dict = load_config(config)
    config = Config(config_dict)

    return config
