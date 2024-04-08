"""Get data from psql"""

# flake8: noqa E501

# import asyncio
import json
import os

import psycopg
import psycopg_infdate
import yaml
from icecream import ic
from psycopg.rows import dict_row

from commands import commands as cmd
from config import ignores, inputs_dir

# DEBUG_DB_INCLUDE_ONLY = ["dev-wallet"]
# DEBUG_DB_NUM = 2
DEBUG_DB_INCLUDE_ONLY = []
DEBUG_DB_NUM = None

result = {}

psycopg_infdate.register_inf_date_handler(psycopg)


def get_something(cur, sql, ignore_columns, ignore_rows=None):
    """Common func to get something from psql"""

    something = {}
    cur.execute(sql)
    for row in cur:
        name = row[ignore_columns[0]]
        for ignore_column in ignore_columns:
            del row[ignore_column]
        something[name] = dict(row)
    if ignore_rows is not None:
        for r in ignore_rows:
            if r in something:
                del something[r]
    return something


def get_tables_info(
    input_, instance, dbname, user, host, password
):  # pylint: disable=too-many-arguments, too-many-locals
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

    tables_info = {}
    conn_str = f"{dbname=} {user=} {host=} {password=} connect_timeout=3"
    # with psycopg.AsyncConnection.connect(
    with psycopg.connect(  # pylint: disable=not-context-manager
        conn_str, row_factory=dict_row
    ) as conn:
        with conn.cursor() as cur:
            schemas = get_schemas(cur)
            ic(input_, instance, dbname, list(schemas))
            for schema in schemas:
                ic(input_, instance, dbname, schema)

                owners = get_owners(cur, schema)
                owners_empty = not bool(owners)
                ic(input_, instance, dbname, schema, owners_empty)

                tables_perm = get_tables_perms(cur, schema)
                tables_perm_empty = not bool(tables_perm)
                ic(input_, instance, dbname, schema, tables_perm_empty)

                # merge owners to tables_perm
                for table, vals in owners.items():
                    tables_perm[table] |= vals

                # drop not type=table items, drop Type proper
                for table in list(tables_perm):
                    type_ = tables_perm[table]["Type"]
                    del tables_perm[table]["Type"]
                    if type_ != "table":
                        del tables_perm[table]

                if tables_perm:
                    tables_info[schema] = tables_perm
    result[input_][instance]["databases"][dbname]["Schemas"] = tables_info


def get_instance_info(
    what, input_, instance, dbname, user, host, password
):  # pylint: disable=too-many-arguments
    """Get info about instance: databases and roles"""

    def get_databases(cur):
        return get_something(cur, cmd.l, ["Name"], ignores.db)

    def get_roles(cur):
        return get_something(cur, cmd.du, ["rolname"], ignores.role)

    instance_info = {}
    conn_str = f"{dbname=} {user=} {host=} {password=} connect_timeout=3"
    ic(input_, instance, conn_str)
    # with psycopg.AsyncConnection.connect(
    with psycopg.connect(  # pylint: disable=not-context-manager
        conn_str, row_factory=dict_row
    ) as conn:
        with conn.cursor() as cur:
            if what != "roles":
                databases = get_databases(cur)
                if DEBUG_DB_INCLUDE_ONLY:
                    for db in list(databases):
                        if db not in DEBUG_DB_INCLUDE_ONLY:
                            del databases[db]
                instance_info["databases"] = databases
            if what != "databases":
                instance_info["roles"] = get_roles(cur)

    result[input_][instance] = instance_info


def process_instance(input_, instance, conn_info, what, count_str_instance):
    """Get data for instance"""

    get_instance_info(what, input_, instance, **conn_info)

    if what != "roles":
        databases = result[input_][instance]["databases"]
        databases_number = len(databases)
        ic(databases_number)

        # block for useless log output
        for count, dbname in enumerate(list(databases)[:DEBUG_DB_NUM]):
            if DEBUG_DB_INCLUDE_ONLY and dbname not in DEBUG_DB_INCLUDE_ONLY:
                continue

            count_str_db = (
                f"{count+1:{0}{len(str(databases_number))}}/{databases_number}"
            )
            ic(input_, instance, count_str_instance, dbname, count_str_db)

            get_tables_info(
                **conn_info | {"input_": input_, "instance": instance, "dbname": dbname}
            )

        # asyncio.gather(
        #     *(
        #         get_tables_info(
        #             **conn_info
        #             | {"input_": input_, "instance": instance, "dbname": dbname}
        #         )
        #         for dbname in list(databases)[:DEBUG_DB_NUM]
        #     )
        # )


def process_input_(input_, instances, what):
    """Get data for input"""

    # add root user to ignore roles list
    # for conn_info in instances.values():
    #     ignores.role.append(conn_info["user"])

    # asyncio.gather(
    #     *(
    #         process_instance(input_, instance, conn_info, what)
    #         for instance, conn_info in instances.items()
    #     )
    # )
    instances_number = len(instances.keys())
    ic(input_, instances_number)
    for count, (instance, conn_info) in enumerate(instances.items()):
        count_str_instance = (
            f"{count+1:{0}{len(str(instances_number))}}/{instances_number}"
        )
        process_instance(input_, instance, conn_info, what, count_str_instance)


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


def get_data_from_psql(what):
    """Get databases and roles info main func"""

    inputs_dict = {}
    for file_name in os.listdir(inputs_dir):
        input_ = os.path.splitext(file_name)[0]
        if input_ in ignores.inputs:
            continue
        inputs_dict[input_] = get_instances(file_name)

    # asyncio.gather(
    #     *(
    #         process_input_(input_, instances, what)
    #         for input_, instances in inputs_dict.items()
    #     )
    # )

    for input_, instances in inputs_dict.items():
        result[input_] = {}
        process_input_(input_, instances, what)
    return ic(result)


# def get_data_from_psql(what):
#     """Fire for async_get_data_from_psql func"""

#     asyncio.run(async_get_data_from_psql(what))
#     ic(result)
#     return result
