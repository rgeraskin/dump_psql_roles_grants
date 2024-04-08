"""
This module serves as the entry point for the dump_psql_roles_grants application.

It imports the `cli` function from the `dump_psql_roles_grants.cli` module and calls
it when the script is executed.
"""

from dump_psql_roles_grants.cli import cli

if __name__ == "__main__":
    cli()
