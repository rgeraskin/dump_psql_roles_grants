#!/usr/bin/env python3
"""Print and dump results in table view"""

import pytablewriter
from icecream import ic

from config import HEADER_DB, HEADER_ROLES, ignores


def get_table_formats():
    """Get supported TableWriters in pytablewriter"""

    formats = []
    for elem in dir(pytablewriter):
        if elem.endswith("TableWriter"):
            formats.append(elem.rstrip("TableWriter"))
    return formats


def fill_ignored_indices(header, ignored_cols):
    """Convert ignored header names into indices"""

    ic.enable()
    ignored_indices = []
    for ignored_col in ignored_cols:
        index = header.index(ignored_col)
        ignored_indices.append(index)
    return ic(ignored_indices)


def table_filter(header, ignored_indices, rows):
    """Remove ignored columns from table"""

    f_header = [x for x in header if header.index(x) not in ignored_indices]
    f_rows = []
    for row in rows:
        for col in sorted(ignored_indices, reverse=True):
            _ = row.pop(col)
        f_rows.append(row)
    return f_header, f_rows


def table_gen_roles(roles, rows, row):
    """Role specific table gen"""

    role_column = len(row)
    for role, role_props in roles.items():
        row.append(ic(role))
        row.append(ic(role_props["rolbypassrls"]))
        row.append(ic(role_props["rolcanlogin"]))
        row.append(ic(role_props["rolconnlimit"]))
        row.append(ic(role_props["rolcreatedb"]))
        row.append(ic(role_props["rolcreaterole"]))
        row.append(ic(role_props["rolinherit"]))
        row.append(ic(role_props["rolreplication"]))
        row.append(ic(role_props["rolsuper"]))
        row.append(ic(role_props["rolvaliduntil"]))
        row.append(ic("\n".join(role_props["memberof"])))
        rows.append(ic(row))
        row = row[:role_column]
    return row[: role_column - 1]


def table_gen_dbs(databases, rows, row):
    """Database specific table gen"""

    for db, db_props in databases.items():
        row.append(ic(db))
        row.append(ic(db_props["Owner"]))
        row.append(ic(db_props["Access privileges"]))

        for schema, tables in db_props["Schemas"].items():
            row.append(ic(schema))

            schema_column = len(row)
            for table, table_props in tables.items():
                row.append(ic(table))
                row.append(ic(table_props.get("Owner")))
                row.append(ic(table_props.get("Access privileges")))
                row.append(ic(table_props.get("Column privileges")))
                row.append(ic(table_props.get("Policies")))

                rows.append(ic(row))
                row = row[:schema_column]
            row = row[: schema_column - 1]
    return row


def table_gen(conts, entity, entity_func, header, ignored_cols):
    """Generate common part of a table"""

    ignored_indices = fill_ignored_indices(header, ignored_cols)
    ic.disable()

    rows = []
    for input_, instances in conts.items():
        row = []
        row.append(ic(input_))

        for instance, entities in instances.items():
            row.append(ic(instance))
            row = entity_func(entities[entity], rows, row)

    header, rows = table_filter(header, ignored_indices, rows)
    # print(len(header), header)
    # for row in rows:
    #     print(len(row), row)
    # print()
    return header, rows


def table_write(
    table_name,
    headers,
    value_matrix,
    print_=False,
    dump=False,
    fmt="Markdown",
):
    """Print and dump results in table view implementation"""

    writer = getattr(pytablewriter, f"{fmt}TableWriter")(
        table_name=table_name.capitalize(),
        headers=headers,
        value_matrix=value_matrix,
        margin=1,
    )
    if print_:
        writer.write_table()
    if dump:
        writer.dump(f"{table_name}.{fmt.lower()}")


def dump_table(print_, what, data, fmt):
    """Print and dump results in table view main func"""

    entities = {
        "databases": {
            "entity_func": table_gen_dbs,
            "header": HEADER_DB,
            "ignored_cols": ignores.result_table_column_databases,
        },
        "roles": {
            "entity_func": table_gen_roles,
            "header": HEADER_ROLES,
            "ignored_cols": ignores.result_table_column_roles,
        },
    }

    if what == "roles":
        del entities["databases"]
    elif what == "databases":
        del entities["roles"]

    for entity, vals in entities.items():
        headers, rows = table_gen(**(vals | {"conts": data, "entity": entity}))
        if print_:
            table_write(entity, headers, rows, print_=True, fmt="Markdown", dump=False)
        if fmt:
            table_write(entity, headers, rows, print_=False, fmt=fmt, dump=True)
