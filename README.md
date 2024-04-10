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
CREATE USER my_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE yahoo_search_engine TO my_user;
```

## Setup the environment variables used in `alembic.ini`

```commandline
export DB_USER=my_user
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

## Spin up server locally on port 8080

```commandline
python src/main.py
```

## Sample Requests

### Hello World

GET http://localhost:8080/hello_world

#### Output

```text
Hello World
```

### Create User

POST http://localhost:8080/create_user

#### Output

```json
{
	"user_id": "ace97aa8-e5e4-4fbd-b2dd-1a5fec9a2e20",
	"created_at": "2024-04-08 15:37:31"
}
```

![Hello World](./images/hello_world.png)

### Search

POST http://localhost:8080/search

#### Input

```json
{
	"user_id": "ace97aa8-e5e4-4fbd-b2dd-1a5fec9a2e20",
	"query": "tea"
}
```

![Create User](./images/create_user.png)

#### Output

```json
{
	"search_id": "14e197bc-ecf8-413f-a89a-23174ae938a8",
	"user_id": "ace97aa8-e5e4-4fbd-b2dd-1a5fec9a2e20",
	"search_term": "tea",
	"result": "MASSIVE_HTML_HERE",
	"created_at": "2024-04-08 15:38:03"
}
```

![Search](./images/search.png)

## Run Unit Tests

```
pytest unit_tests
```

## Run Integration Tests

### Step 1: Setup the environment variables used in `alembic.ini`

```commandline
export DB_USER=it_user
export DB_PASSWORD=it_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_DATABASE=it_yahoo_search_engine
```

### Step 2: Create database + it_user

```commandline
CREATE DATABASE it_yahoo_search_engine;
CREATE USER it_user WITH PASSWORD 'it_password';
GRANT ALL PRIVILEGES ON DATABASE it_yahoo_search_engine TO it_user;
```

### Step 3: Use alembic to create integration test tables and database

```commandline
alembic upgrade head
```

### Step 4: Run the integration tests

```commandline
pytest -p no:asyncio --max-asyncio-tasks 1 integration_tests
```

## Future work

It can be further extended to give back images, or summarize / recommend searches later

## TODOs:
- [x] Wire up services to an async server; aiohttp
- [x] Write unit tests
- [x] Write integration tests
- [ ] Integrate Redis to do distributed caching
- [ ] Train and implement NLP model to parse the results into structured data (JSON) 