# ARQUISOFT - ofipensiones - ISIS-2503

## docker compose management

```
sudo docker compose up [-d]
sudo docker compose down -v
```

in case of rebuilding images

```
sudo docker compose up --build --force-recreate
```

## get healthcheck logs

```
sudo docker inspect --format "{{json .State.Health }}" <name> | jq
```

## inspect volumes

```
docker volume inspect <volume_name>
```

## psql

```
docker compose exec pgdb psql --username=<> --dbname=<>

```

## django manage

```
cd docker/django_manage && sudo docker compose up
sudo docker exec -it <container_id> sh
uv run --no-cache ofipensiones/manage.py
```

# perform migrations

```
. dj_manage_env.sh
uv run ofipensiones/manage.py makemigrations
uv run ofipensiones/manage.py migrate
```

## nginx logs

Stored at `/var/log/nginx`. By default Nginx has `access_log` and `error_log`
properties.

## Note on gunicorn tuning

Gunicorn offers 3 models:

- sync (fork process)
- async
- Gtrhead (fork process w/ threads)

Usually when an app is running on a dedicated server it is recommended to have
`2 * CPU + 1` workers.

On `IO` bound tasks it would be better to use an async model, as it can suspend
easily without consuming much resources. Meanwhile process fork is recommended
for `COMPUTE` bound tasks.

Note that Gthread is an optimization for space, but has the restriction of
python threading implementation `GIL`.

## NGINX

`location = <path> {}` vs `location <path> {}`

The first is an exact match while the latter is a prefix match.

## Miembros

- Andres Juan Cardenas Layton - a.cardenasl@uniandes.edu.co - 202122083
- Isaac David Bermudez Lara - i.bermudezl@uniandes.edu.co - 202014146
- SSantiago Tenjo Venegas - s.tenjov@uniandes.edu.co - 202113965
- Samara Martinez Jacome -  s.martinezj@uniandes.edu.co - 202221057
