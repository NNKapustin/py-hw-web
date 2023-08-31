
run all
```shell
docker-compose --env-file .env.inttest up
```

run redis
```shell
docker-compose --env-file .env.inttest up redis
```

run app
```shell
docker-compose --env-file .env.inttest up app
```

run celery
```shell
docker-compose --env-file .env.inttest up celery
```

run celery
```shell
docker-compose --env-file .env.inttest up tests
```
