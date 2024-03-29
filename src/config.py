"""Configuration-related things"""

import yaml

from classes import Ignores

CONFIG_FILE = "config.yaml"

HEADER_DB = [
    "Env",
    "Instance name",
    "Database",
    "Owner",
    "Access privileges",
    "Schema",
    "Table",
    "Table owner",
    "Access privileges",
    "Column privileges",
    "Policies",
]

HEADER_ROLES = [
    "Env",
    "Instance name",
    "Role name",
    "rolbypassrls",
    "rolcanlogin",
    "rolconnlimit",
    "rolcreatedb",
    "rolcreaterole",
    "rolinherit",
    "rolreplication",
    "rolsuper",
    "rolvaliduntil",
    "memberof",
]


def load_config(conf_file):
    """Load config from file"""

    with open(conf_file, "r", encoding="utf8") as f:
        conf = yaml.safe_load(f)
    return conf


_config = load_config(CONFIG_FILE)
ignores = Ignores(**_config["ignores"])
inputs_dir = _config["inputs_dir"]
results_dir = _config["results_dir"]
