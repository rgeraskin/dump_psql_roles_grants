# Dump Postgres Roles and Grants

## Build

```shell
docker buildx build -t dump_psql_roles_grants .
```

## Usage

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
   docker run -it --rm -v ${PWD}/_inputs:/app/_inputs -v ${PWD}/_results:/app/_results dump_psql_roles_grants -- --help
   ```
