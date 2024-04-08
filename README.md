# Dump Postgres Roles and Grants

## Install

### pipx

```shell
pipx install dump-psql-roles-grants
dump-psql-roles-grants --help
```

### pip

```shell
pip install dump-psql-roles-grants
python -m dump_psql_roles_grants --help
```

### docker

```shell
docker pull rgeraskin/dump_psql_roles_grants
docker run --name dump_psql_roles_grants --rm rgeraskin/dump_psql_roles_grants --help
```

## Usage

1. Generate an example config file `dump_psql_roles_grants gen-example-config -o config.yaml`
1. Place instances connection info to `_inputs` dir

   ```shell
   _inputs/
   ├── dev.yaml
   ├── prod.yaml
   ├── stage.yaml
   └── test.yaml
   ```

   File format: yaml or json

   ```yaml
   <INSTANCE NAME 1>:
     dbname: <DB TO CONNECT>
     host: <INSTANCE HOSTNAME>
     password: <PASSWORD>
     user: <USER NAME>

   <INSTANCE NAME X>:
     dbname: <DB TO CONNECT>
     host: <INSTANCE HOSTNAME>
     password: <PASSWORD>
     user: <USER NAME>
   ```

1. Review `config.yaml`

1. Run

   ```shell
   dump_psql_roles_grants --help
   ```
