# pylint: disable=missing-module-docstring

from classes import Ignores

inputs_dir = "./inputs"

ignores = Ignores(
    inputs=[
        "stage",
        "test",
        "prod",
    ],
    db=[
        "postgres",
        "rdsadmin",
        "template0",
        "template1",
    ],
    role=[
        "rdstopmgr",
        "rdsrepladmin",
        "rdsadmin",
        "rds_superuser",
        "rds_replication",
        "rds_password",
        "rds_iam",
        "rds_ad",
        "datadog_agent",
        "change_owner",
    ],
    schema=[
        "pg_catalog",
        "information_schema",
        "datadog",
    ],
    table=[
        "pg_stat_statements",
    ],
)
