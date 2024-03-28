"""Get data from psql"""

# flake8: noqa E501

import json
import os

import psycopg2
import psycopg2.extras
import yaml
from icecream import ic

from commands import commands as cmd
from config import ignores, inputs_dir

DEBUG_DB_INCLUDE_ONLY = ["dev-wallet"]
DEBUG_DB_NUM = 20
# DEBUG_DB_INCLUDE_ONLY = []
# DEBUG_DB_NUM = None


def get_something(cur, sql, ignore_columns, ignore_rows=None):
    """Common func to get something from psql"""

    something = {}
    cur.execute(sql)
    for row in cur.fetchall():
        name = row[ignore_columns[0]]
        for ignore_column in ignore_columns:
            del row[ignore_column]
        something[name] = dict(row)
    if ignore_rows is not None:
        for r in ignore_rows:
            if r in something:
                del something[r]
    return something


def get_instance_info(what, dbname, user, host, password):
    """Get info about instance: databases and roles"""

    def get_databases(cur):
        return get_something(cur, cmd.l, ["Name"], ignores.db)

    def get_roles(cur):
        return get_something(cur, cmd.du, ["rolname"], ignores.role)

    instance_info = {}
    conn_str = f"{dbname=} {user=} {host=} {password=} connect_timeout=3"
    with psycopg2.connect(conn_str) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if what != "roles":
                databases = get_databases(cur)
                if DEBUG_DB_INCLUDE_ONLY:
                    for db in list(databases):
                        if db not in DEBUG_DB_INCLUDE_ONLY:
                            del databases[db]
                instance_info["databases"] = databases
            if what != "databases":
                instance_info["roles"] = get_roles(cur)

    return instance_info


def get_tables_info(dbname, user, host, password):
    """Get info about tables: schemas, owners, perms"""

    def get_schemas(cur):
        ignore_columns = ["Name"]
        return get_something(cur, cmd.get_schemas, ignore_columns, ignores.schema)

    def get_owners(cur, schema):
        cmddt = (cmd.dt).replace("PLACEHOLDER", schema)
        ignore_columns = ["Name", "Type", "Schema"]
        return get_something(cur, cmddt, ignore_columns)

    def get_tables_perms(cur, schema):
        cmdz = (cmd.z).replace("PLACEHOLDER", schema)
        ignore_columns = ["Name", "Schema"]
        return get_something(cur, cmdz, ignore_columns, ignores.table)

    ic.disable()
    tables_info = {}
    conn_str = f"{dbname=} {user=} {host=} {password=} connect_timeout=3"
    with psycopg2.connect(conn_str) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            schemas = get_schemas(cur)
            for schema in ic(schemas):
                ic(schema)
                owners = ic(get_owners(cur, schema))
                tables_perm = ic(get_tables_perms(cur, schema))
                for table in owners:
                    tables_perm[table] |= owners[table]
                for table in list(tables_perm):
                    type_ = tables_perm[table]["Type"]
                    del tables_perm[table]["Type"]
                    if type_ != "table":
                        del tables_perm[table]
                if tables_perm:
                    tables_info[schema] = tables_perm
    return tables_info


def get_data_from_psql(print_, what):
    """Get databases and roles info"""

    result = {}
    for file_name in os.listdir(inputs_dir):
        input_ = os.path.splitext(file_name)[0]
        if input_ in ignores.inputs:
            continue
        result[input_] = {}

        instances = get_instances(file_name)

        for instance, conn_info in instances.items():
            ignores.role.append(conn_info["user"])
            instance_info = get_instance_info(what, **conn_info)
            result[input_][instance] = instance_info

            if what != "roles":
                databases = result[input_][instance]["databases"]
                databases_number = len(databases)
                ic(databases_number)
                for count, dbname in enumerate(list(databases)[:DEBUG_DB_NUM]):
                    if DEBUG_DB_INCLUDE_ONLY and dbname not in DEBUG_DB_INCLUDE_ONLY:
                        continue
                    count_str = f"{count:03}/{databases_number}"
                    ic(count_str, dbname)
                    databases[dbname]["Schemas"] = get_tables_info(
                        **conn_info | {"dbname": dbname}
                    )  # pylint: disable=undefined-loop-variable

    if print_:
        ic.enable()
        ic(result)
    return result


def get_instances(file_name):
    """Get data from input files"""

    with open(os.path.join(inputs_dir, file_name), encoding="utf8") as f:
        ext = os.path.splitext(file_name)[1]
        if ext == ".json":
            instances = json.load(f)
        elif ext == ".yaml":
            instances = yaml.safe_load(f)
        else:
            raise IOError(f"Not supported format for '{file_name}'")
    return instances
