#!/usr/bin/env python
"""Command line interface"""

import click

from dump_psql_roles_grants.classes import Ignores
from dump_psql_roles_grants.config import load_config
from dump_psql_roles_grants.get_data import get_data_from_psql
from dump_psql_roles_grants.table import dump_table

# from table import get_table_formats


@click.group()
# @click.option("-v", "--verbose", count=True)
def cli():
    """Dump Postgres Roles and Grants"""


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
@click.option(
    "--config",
    "-c",
    default="config.yaml",
    show_default=True,
    help="config file to use",
)
def export(print_, what, dump_in_format, config):
    """Export instance data"""

    _config = load_config(config)
    ignores = Ignores(**_config["ignores"])
    inputs_dir = _config["inputs_dir"]
    results_dir = _config["results_dir"]

    data = get_data_from_psql(what, inputs_dir, ignores)

    dump_table(print_, what, data, dump_in_format, results_dir, ignores)


@cli.command()
@click.option(
    "--output",
    "-o",
    show_default=True,
    help="file to write example config to",
)
def gen_example_config(output=None):
    """Generate example config file"""

    example_config = """
# Example config file

inputs_dir: ./_inputs
results_dir: ./_results
ignores:
  inputs:
    # []
    - dev
    # - stage
    - test
    - prod
  db:
    - postgres
    - rdsadmin
    - template0
    - template1
  role:
    - rdstopmgr
    - rdsrepladmin
    - rdsadmin
    - rds_superuser
    - rds_replication
    - rds_password
    - rds_iam
    - rds_ad
    - datadog_agent
    - change_owner
  schema:
    - pg_catalog
    - information_schema
    - datadog
  table:
    - pg_stat_statements
  result_table_column_databases:
    []
    # - Env
    # - Instance name
    # - Database
    # - Owner
    # - Access privileges
    # - Schema
    # - Table
    # - Table owner
    # - Access privileges
    # - Column privileges
    # - Policies
  result_table_column_roles:
    []
    # - Env
    # - Instance name
    # - Role name
    # - rolbypassrls
    # - rolcanlogin
    # - rolconnlimit
    # - rolcreatedb
    # - rolcreaterole
    # - rolinherit
    # - rolreplication
    # - rolsuper
    # - rolvaliduntil
    # - memberof
""".lstrip()

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(example_config)
    else:
        click.echo(example_config)
