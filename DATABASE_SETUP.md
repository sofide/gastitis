# Setup databae in postgres container

## Run a postgres container

- To download latest image:
```bash
docker pull postgres
```

- To see the downloaded image:
```bash
docker images
```

- To run a container with a fixed volume in `postgres-datadir`
```
docker run -d \
    --name postgres-sofi \
    -e POSTGRES_PASSWORD=<secret-password> \
    -v </path/until/local/directory/volume>:/var/lib/postgresql/data \
    -v </path/until/local/directory/volume>:/backups \
    -p 5432:5432 \
    postgres
```

- To access a shell inside postgres container, we can use psql:

```bash
docker exec -it postgres-sofi  psql -U postgres --help
```

The `-U postgres` param can be omited in the command `--help`, but it's needed in all
the other commands to manipulate the database.

You can use psql to create a new `gastitis` database or restore a backup.

## Check out existing databases
```bash
docker exec -it postgres-sofi psql -U postgres -c "SELECT datname FROM pg_database"
```

## Create a new database

```bash
docker exec -it postgres-sofi psql -U postgres -c "CREATE DATABASE gastitis"
```

## Restore a backup

To restore a backup:

- First, we need to make sure we have the correct volumes mounted. We can inspect that
with the following command:

```bash
docker inspect -f '{{ json .Mounts }}' postgres-sofi
```

- first, copy the dump in our `/backups` folder (thanks to the volume created in `run`)
```bash
docker cp <backup_path> postgres-sofi:backups
```

- then, restore it with `pg_restore`:
```bash
docker exec -it postgres-sofi pg_restore \
    --verbose --clean --no-acl --no-owner \
    -h localhost 
    -U postgres
    -d gastitis \
    backups/<backup_name>
```

### Make a Query

To check everything is loaded as expected, we can run a query with pysql:
```bash
docker exec -it postgres-sofi \
    psql -U postgres -d gastitis -s public \
    -c "SELECT * FROM expenses_expense ORDER BY id DESC LIMIT 100"
```

## Check out existing users (or roles)
```bash
docker exec -it postgres-sofi psql -U postgres -c "SELECT rolname FROM pg_roles"
```

## Create a user
```bash
docker exec -it postgres-sofi psql -U postgres -d gastitis -c "CREATE ROLE your_user WITH LOGIN PASSWORD 'your_password'"
docker exec -it postgres-sofi psql -U postgres -d gastitis -c "GRANT ALL ON DATABASE gastitis TO your_user"
docker exec -it postgres-sofi psql -U postgres -d gastitis -c "GRANT ALL ON ALL SCHEMA public TO your_user"
```

## Change the ownership of a table
```bash
docker exec -it postgres-sofi psql -U postgres -d gastitis -s public -c "ALTER TABLE bot_telegramgroup OWNER TO your_user"
```
