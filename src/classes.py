# pylint: disable=missing-module-docstring,missing-class-docstring
from dataclasses import dataclass


@dataclass
class Commands():
    dt: str
    du: str
    get_schemas: str
    l: str
    z: str


@dataclass
class Ignores():
    db: list
    inputs: list
    role: list
    schema: list
    table: list
