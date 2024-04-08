"""Configuration-related things"""

import yaml

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

    try:
        with open(conf_file, "r", encoding="utf8") as f:
            conf = yaml.safe_load(f)
    except FileNotFoundError as exc:
        raise SystemExit(
            f"Config file {conf_file} not found. "
            "You can create it with `dump_psql_roles_grants gen-example-config`"
        ) from exc
    return conf
