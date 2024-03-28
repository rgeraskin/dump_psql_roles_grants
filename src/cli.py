#!/usr/bin/env python
"""Command line interface"""

import click

from get_data import get_data_from_psql
from table import dump_table, get_table_formats


@click.group()
# @click.option("-v", "--verbose", count=True)
def cli():
    """CLI group function"""


@cli.command()
@click.option(
    "--print/--no-print",
    "print_",
    is_flag=True,
    show_default=True,
    default=True,
    help="display results",
)
@click.option(
    "--what",
    "-w",
    default="all",
    type=click.Choice(["all", "databases", "roles"]),
    show_default=True,
    help="what to export",
)
@click.option(
    "--dump-in-format",
    "-f",
    default="Csv",
    type=click.Choice(get_table_formats()),
    help="dump results in specified table format",
)
def export(print_, what, dump_in_format):
    """Export instance data"""

    data = get_data_from_psql(what)

    dump_table(print_, what, data, dump_in_format)


if __name__ == "__main__":
    cli()
