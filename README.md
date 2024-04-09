# Dump Postgres Roles and Grants

## Install

You can choose

- plain python package `dump-psql-roles-grants` that requires `libpq` system library
- or package `dump-psql-roles-grants[binary]` that have binaries included

### pipx (preferred)

```shell
pipx install 'dump-psql-roles-grants[binary]'
dump_psql_roles_grants --help
```

### brew

```shell
brew install rgeraskin/homebrew/dump-psql-roles-grants
dump_psql_roles_grants --help
```

### pip

```shell
pip install 'dump-psql-roles-grants[binary]'
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
