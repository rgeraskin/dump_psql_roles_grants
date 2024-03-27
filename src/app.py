#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-function-docstring,unspecified-encoding
# flake8: noqa E501

import json
import os

import psycopg2
import psycopg2.extras
from icecream import ic

from commands import commands as cmd
from config import ignores, inputs_dir

DEBUG_DB_INCLUDE_ONLY = ["dev-wallet"]
DEBUG_DB_NUM = 20
# DEBUG_DB_INCLUDE_ONLY = []
# DEBUG_DB_NUM = None


def get_something(cur, sql, ignore_columns, ignore_rows=None):
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


def get_instance_info(dbname, user, host, password):

    def get_databases(cur):
        return get_something(cur, cmd.l, ["Name"], ignores.db)

    def get_roles(cur):
        return get_something(cur, cmd.du, ["rolname"], ignores.role)

    conn_str = f"{dbname=} {user=} {host=} {password=} connect_timeout=3"
    with psycopg2.connect(conn_str) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            databases = get_databases(cur)
            if DEBUG_DB_INCLUDE_ONLY:
                for db in list(databases):
                    if db not in DEBUG_DB_INCLUDE_ONLY:
                        del databases[db]

            instance_info = {"databases": databases, "roles": get_roles(cur)}
    return instance_info


def get_tables_info(dbname, user, host, password):

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
                    tables_perm[table] = tables_perm[table] | owners[table]
                # for table in list(tables_perm):
                #     if (tables_perm[table]['Access privileges'] is None
                #             and tables_perm[table]['Column privileges'] == ''
                #             and tables_perm[table]['Policies'] == ''):
                #         del tables_perm[table]
                if tables_perm:
                    tables_info[schema] = tables_perm
    return tables_info


def main():
    result = {}
    for file_name in os.listdir(inputs_dir):
        input_ = os.path.splitext(file_name)[0]
        if input_ in ignores.inputs:
            continue

        with open(os.path.join(inputs_dir, file_name)) as f:
            instances = json.load(f)

        for _, conn_info in instances.items():
            ignores.role.append(conn_info["user"])
            instance_info = get_instance_info(**conn_info)
            result[input_] = instance_info

            databases = result[input_]["databases"]
            databases_number = len(databases)
            ic(databases_number)
            for count, dbname in enumerate(list(databases)[:DEBUG_DB_NUM]):
                if DEBUG_DB_INCLUDE_ONLY and dbname not in DEBUG_DB_INCLUDE_ONLY:
                    continue
                count_str = f"{count:03}/{databases_number}"
                ic(count_str, dbname)
                result[input_]["databases"][dbname]["schemas"] = get_tables_info(
                    **conn_info | {"dbname": dbname}
                )  # pylint: disable=undefined-loop-variable
    return result


if __name__ == "__main__":
    res = main()
    ic.enable()
    ic(res)
