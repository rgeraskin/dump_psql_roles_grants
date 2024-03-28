#!/usr/bin/env python
"""Command line interface"""

import click

from get_data import get_data_from_psql


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
# @click.option(
#     "--dump-in-format",
#     "-f",
#     type=click.Choice(["csv", "xlsx", "yaml"]),
#     help="dump results in specified format",
# )
def export(
    print_,
    what,
    # dump_in_format,
):
    """Export instance data"""

    get_data_from_psql(print_, what)
    # if dump_in_format:
    #     logging.error("Not implemented")


if __name__ == "__main__":
    cli()
