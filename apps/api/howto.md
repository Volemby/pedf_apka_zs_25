
## Login to the database:
-- docker compose -f infra/docker-compose.yml exec db psql -U app -d app

## Viewing the database
-- docker compose -f infra/docker-compose.yml exec db psql -U app -d app


## Connection info
vojtechhorak@BOSS appka_zs_25 % PGPASSWORD=app psql -h localhost -p 5432 -U app -d app -c "\conninfo"
You are connected to database "app" as user "app" on host "localhost" (address "::1") at port "5432".