#!/usr/bin/env python
"""Command line interface"""

import click

from dump_psql_roles_grants.get_data import get_data_from_psql
from dump_psql_roles_grants.table import dump_table

# from table import get_table_formats


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
    # type=click.Choice(get_table_formats()),
    type=click.Choice(
        [
            "Abstrac",
            "AsciiDoc",
            "BoldUnicod",
            "Borderless",
            "Css",
            "Csv",
            "ExcelXls",
            "ExcelXlsx",
            "Htm",
            "JavaScrip",
            "JsonLines",
            "Json",
            "Latex",
            "Ltsv",
            "Markdown",
        ]
    ),
    help="dump results in specified table format",
)
def export(print_, what, dump_in_format):
    """Export instance data"""

    data = get_data_from_psql(what)

    dump_table(print_, what, data, dump_in_format)
