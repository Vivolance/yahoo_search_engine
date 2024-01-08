# Google Search Engine aPI

This repository houses a powerful python API service, able to make google searches on behalf of it's users

It then parses the results and display the top 10 search results and their titles and links.

## Python Version: 3.10

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