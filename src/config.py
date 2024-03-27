# pylint: disable=missing-module-docstring,missing-function-docstring
# pylint: disable=unspecified-encoding

import yaml

from classes import Ignores

CONFIG_FILE = "config.yaml"


def load_config(conf_file):
    with open(conf_file, "r") as f:
        conf = yaml.safe_load(f)
    return conf


_config = load_config(CONFIG_FILE)
ignores = Ignores(**_config["ignores"])
inputs_dir = _config["inputs_dir"]
