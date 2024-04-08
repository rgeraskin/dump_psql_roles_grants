# pylint: disable=missing-module-docstring
# flake8: noqa E501

from dump_psql_roles_grants.classes import Commands

commands = Commands(
    # \l
    l="""
    SELECT
      d.datname as "Name",
      pg_catalog.pg_get_userbyid(d.datdba) as "Owner",
      pg_catalog.array_to_string(d.datacl, E'\n') AS "Access privileges"
    FROM pg_catalog.pg_database d
    ORDER BY 1;
    """,
    # \du
    du="""
    SELECT r.rolname, r.rolsuper, r.rolinherit,
      r.rolcreaterole, r.rolcreatedb, r.rolcanlogin,
      r.rolconnlimit, r.rolvaliduntil,
      ARRAY(SELECT b.rolname
            FROM pg_catalog.pg_auth_members m
            JOIN pg_catalog.pg_roles b ON (m.roleid = b.oid)
            WHERE m.member = r.oid) as memberof
    , r.rolreplication
    , r.rolbypassrls
    FROM pg_catalog.pg_roles r
    WHERE r.rolname !~ '^pg_'
    ORDER BY 1;
    """,
    dt="""
    SELECT n.nspname as "Schema",
      c.relname as "Name",
      CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' WHEN 't' THEN 'TOAST table' WHEN 'f' THEN 'foreign table' WHEN 'p' THEN 'partitioned table' WHEN 'I' THEN 'partitioned index' END as "Type",
      pg_catalog.pg_get_userbyid(c.relowner) as "Owner"
    FROM pg_catalog.pg_class c
         LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
         LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam
    WHERE c.relkind IN ('r','p','t','s','')
      AND n.nspname OPERATOR(pg_catalog.~) '^(PLACEHOLDER)$' COLLATE pg_catalog.default
    ORDER BY 1,2;
    """,
    get_schemas="""
    SELECT schema_name as "Name"
    FROM information_schema.schemata;
    """,
    z="""
    SELECT n.nspname as "Schema",
      c.relname as "Name",
      CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'S' THEN 'sequence' WHEN 'f' THEN 'foreign table' WHEN 'p' THEN 'partitioned table' END as "Type",
      pg_catalog.array_to_string(c.relacl, E'\n') AS "Access privileges",
      pg_catalog.array_to_string(ARRAY(
        SELECT attname || E':\n  ' || pg_catalog.array_to_string(attacl, E'\n  ')
        FROM pg_catalog.pg_attribute a
        WHERE attrelid = c.oid AND NOT attisdropped AND attacl IS NOT NULL
      ), E'\n') AS "Column privileges",
      pg_catalog.array_to_string(ARRAY(
        SELECT polname
        || CASE WHEN NOT polpermissive THEN
           E' (RESTRICTIVE)'
           ELSE '' END
        || CASE WHEN polcmd != '*' THEN
               E' (' || polcmd::pg_catalog.text || E'):'
           ELSE E':'
           END
        || CASE WHEN polqual IS NOT NULL THEN
               E'\n  (u): ' || pg_catalog.pg_get_expr(polqual, polrelid)
           ELSE E''
           END
        || CASE WHEN polwithcheck IS NOT NULL THEN
               E'\n  (c): ' || pg_catalog.pg_get_expr(polwithcheck, polrelid)
           ELSE E''
           END    || CASE WHEN polroles <> '{0}' THEN
               E'\n  to: ' || pg_catalog.array_to_string(
                   ARRAY(
                       SELECT rolname
                       FROM pg_catalog.pg_roles
                       WHERE oid = ANY (polroles)
                       ORDER BY 1
                   ), E', ')
           ELSE E''
           END
        FROM pg_catalog.pg_policy pol
        WHERE polrelid = c.oid), E'\n')
        AS "Policies"
    FROM pg_catalog.pg_class c
         LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind IN ('r','v','m','S','f','p')
      AND n.nspname OPERATOR(pg_catalog.~) '^(PLACEHOLDER)$' COLLATE pg_catalog.default
    ORDER BY 1, 2;
    """,
)
