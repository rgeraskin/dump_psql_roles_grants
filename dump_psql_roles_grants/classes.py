"""Dataclasses for app to be able to access to props by dot"""

from dataclasses import dataclass


@dataclass
class Commands:
    """Sql commands spec"""

    dt: str
    du: str
    get_schemas: str
    l: str
    z: str


@dataclass
class Ignores:
    """Ignores spec"""

    db: list
    inputs: list
    role: list
    schema: list
    table: list
    result_table_column_databases: list
    result_table_column_roles: list
