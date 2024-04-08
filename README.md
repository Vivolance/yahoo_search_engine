# Yahoo Search Engine API

This repository houses a powerful python API service, able to make yahoo searches on behalf of it's users

It then parses the results and display the top 10 search results and their titles and links.

## Spin up both server + postgres@14 database with a single command:

```commandline
docker-compose -f docker-compose.yml up
```

If you made changes to Dockerfile, and wish to regenerate the Docker image

```
docker-compose -f docker-compose.yml up --build --force-recreate
```

## Connect to docker-hosted psql

```commandline
psql -d yahoo_search_engine -U user -p 5432 -h 0.0.0.0
```

## Python Version: 3.11 and above

## (Optional): Bottom steps not necessary if you are using docker above.

## Creating a Virtual Environment

```commandline
poetry shell
```

## Installing dependencies

```commandline
poetry install
```

## Upgrade dependencies on poetry

Edit `pyproject.toml` to have the new version under `tool.poetry.dependencies`

Create a new file with
- `--no-update` ensures we don't update other dependencies that didn't have a change in dependencies in `pyproject.toml`

```commandline
poetry lock --no-update
```

## Setting up PostgreSQL locally

```commandline
brew install postgresql@14
```

## Spin up Postgres locally at localhost:5432

```commandline
brew services start postgresql@14
```

## Connect to local database

```commandline
psql -d postgres
```

## Delete all containers (useful if you wish to start a docker-hosted postgres with a clean slate)

Containers store the disk-level postgres data.
- Sometimes, its useful to delete containers, to let the images regenerate it, to get a fresh DB

```commandline
docker rm $(docker ps -aq)
```

## Delete all docker images

```commandline
docker rmi $(docker images -q)
```

## Create the database for the project

```sql
CREATE DATABASE yahoo_search_engine;
```

## Create a local user; compatible with alembic in `alembic.ini`

```sql
CREATE USER user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE yahoo_search_engine TO user;
```

## Setup the environment variables used in `alembic.ini`

```commandline
export DB_USER=user
export DB_PASSWORD=password
export DB_HOST=localhost
export DB_PORT=5432
export DB_DATABASE=yahoo_search_engine
```

## Creating a new table in `alembic`

In `database_management/tables.py`, define a new `sqlalchemy.Table`

Ensure the table is linked to the `main_metadata: sqlalchemy.MetaData`
- This lets alembic "register" the new table you create

## Generate alembic revision upgrade / downgrade scripts
- Alembic detects new changes in `tables.py` you make
- For each new change it detects, it creates a revision

To create a new revision after making changes

```commandline
alembic revision --autogenerate -m "Create user and search_results table"
```

## Upgrade our database

```commandline
alembic upgrade head
```

## Format code with black

```commandline
black .
```

## Type-check project with mypy

```commandline
mypy .
```

## Lint for common errors with ruff

```commandline
ruff --fix .
```

## Future work

It can be further extended to give back images, or summarize / recommend searches later

## TODOs:
- [ ] Wire up services to an async server; aiohttp
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Integrate Redis to do distributed caching
- [ ] Train and implement NLP model to parse the results into structured data (JSON) 