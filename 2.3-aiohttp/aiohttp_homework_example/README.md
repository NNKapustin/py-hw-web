run all
```shell
docker-compose  --env-file .env.inttest up
```

run database 
```shell
docker-compose  --env-file .env.inttest up db
```


run migration
```shell
docker-compose  --env-file .env.inttest up migration
```

run app
```shell
docker-compose  --env-file .env.inttest up app
```


run test
```shell
docker-compose  --env-file .env.inttest up tests
```