# Google Search Engine API

This repository houses a powerful python API service, able to make google searches on behalf of it's users

It then parses the results and display the top 10 search results and their titles and links.

## Python Version: 3.11 and above

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

## Running the experimental script

```commandline
python3 experimental_script.py
```

## Future work

It can be further extended to give back images, or summarize / recommend searches later

## TODOs:
- [ ] Use poetry as a better dependency management tool over virtualenv
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Integrate Postgres to store user statistics
- [ ] Integrate Redis to do distributed caching
- [ ] Use async to process requests at scale with a single server (asyncio)