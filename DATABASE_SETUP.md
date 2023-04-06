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
sudo docker run -d \
    --name postgres-sofi \
    -e POSTGRES_PASSWORD=<secret-password> \
    -v </path/until/local/directory/volume>:/var/lib/postgresql/data \
    -v </path/until/local/directory/volume>:/backups \
    -p 5432:5432 \
    postgres
```

- To access a shell inside postgres container, we can use psql:

```bash
sudo docker exec -it postgres-sofi  psql -U postgres --help
```

The `-U postgres` param can be omited in the command `--help`, but it's needed in all
the other commands to manipulate the database.

We can use pysql to create a `gastits` table.

## Restore a backup

To restore a backup:

- First, we need to make sure we have the correct volumes mounted. We can inspect that
with the following command:

```bash
sudo docker inspect -f '{{ json .Mounts }}' postgres-sofi
```

- first, copy the dump in our `/backups` folder (thanks to the volume created in `run`)
```bash
sudo docker cp <backup_path> postgres-sofi:backups
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

## Make a Query

To check everything is loaded as expected, we can run a query with pysql:
```bash
sudo docker exec -it postgres-sofi \
    psql -U postgres -d gastitis -s public \
    -c "SELECT * FROM expenses_expense ORDER BY id DESC LIMIT 100"
```

## Create a user
```bash
sudo docker exec -it postgres-sofi psql -U postgres -d gastitis -s public -c "CREATE ROLE your_user WITH LOGIN PASSWORD 'your_password'"
sudo docker exec -it postgres-sofi psql -U postgres -d gastitis -s public -c "GRANT ALL ON DATABASE gastitis TO your_user"
sudo docker exec -it postgres-sofi psql -U postgres -d gastitis -s public -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO your_user"
sudo docker exec -it postgres-sofi psql -U postgres -d gastitis -s public -c "GRANT ALL ON ALL TABLES IN SCHEMA public TO your_user"
```
