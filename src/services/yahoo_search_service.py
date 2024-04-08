import logging
from urllib.parse import quote
import aiohttp
import requests
from retry import retry
from src.models.search_results import SearchResults
from src.models.user import User
from src.services.yahoo_search_dao import YahooSearchDAO
from src.utils.logging_utils import setup_logging
import asyncio


class YahooSearchService:
    def __init__(self, yahoo_search_dao: YahooSearchDAO = YahooSearchDAO()) -> None:
        self.__logger: logging.Logger = logging.Logger(__name__)
        self.__yahoo_search_dao: YahooSearchDAO = yahoo_search_dao
        setup_logging(self.__logger)

    @staticmethod
    def create_url(search_term: str) -> str:
        """
        Given a search term e.g "menstrual cycle"
        1. Url encode it -> "menstrual+cycle"
        2. Concatenate the base url "https://www.google.com/search?q=" with step 1
        :param search_term:
        :return:
        """
        return f"https://sg.search.yahoo.com/search?q={quote(search_term)}"

    @retry(
        exceptions=requests.exceptions.HTTPError,
        tries=5,
        delay=0.01,
        jitter=(-0.01, 0.01),
        backoff=2,
    )
    async def _search(self, user_id: str, search_term: str) -> SearchResults:
        """
        Jitter -> Prevent the thundering herd problem;
        - Imagine you have 1,000 servers all failing
        - Imagine all of them retry every 1
        second at the same time to the downstream server
        - Your downstream server will die
        - So to spread out the requests to the downstream server,
        we add a random noise to their retry intervals
        - For API calls, we typically use -0.01s to 0.01s (10 ms)

        Exponential Backoff
        - Retry up to 5 times
        - 2nd try -> 0.01 seconds after 1st try
        - 3rd try -> 0.02 seconds after 2nd try
        - 4th try -> 0.04 seconds after 3rd try
        - 5th try -> 0.08 seconds after 4th try

        Makes a request to a google search url

        Step 1: Make the API call
        - You can run into HTTPError; eg wifi go down
        - Log and Retry the query if it raises a HTTPError

        Step 2: response succeeded
        - status code is 400 (we as the client fucked up)
        - 200 (success)
        - 500 (server error, the google search engine fucked up)
        """
        self.__logger.info(f"Started google_search for {search_term}")
        try:
            """
            catch the request get
            you can commonly get intermittent wifi errors
            when we do, we get a HTTPError
            """
            url: str = YahooSearchService.create_url(search_term)
            async with aiohttp.ClientSession() as client:
                async with client.get(url, ssl=False) as response:
                    if response.status == 200:
                        # result is the html
                        result: str = await response.text()
                        search_result = SearchResults.create(
                            user_id=user_id, search_term=search_term, result=result
                        )
                        return search_result
                    else:
                        self.__logger.error(
                            f"Response has a non-200 status code: "
                            f"{response.status} for url: {url}"
                        )
                        return SearchResults.create(
                            user_id=user_id, search_term=search_term, result=None
                        )
        except aiohttp.ClientError as e:
            """
            Simplification: assume that all aiohttp.ClientError is retriable
            """
            self.__logger.error(e)
            raise e

    async def yahoo_search(self, user_id: str, search_term: str) -> SearchResults:
        """
        Does two things:
        - Performs the search
        - Persist result into the database
        """
        try:
            result: SearchResults = await self._search(user_id, search_term)
        except Exception as e:
            self.__logger.error(f"Ran in error {e}")
            result = SearchResults.create(
                user_id=user_id, search_term=search_term, result=None
            )
        await self.__yahoo_search_dao.insert_search(result)
        return result


if __name__ == "__main__":
    search_term: str = "menstrual cycle"
    dao: YahooSearchDAO = YahooSearchDAO()
    dummy_user: User = User.create_user()
    asyncio.run(dao.insert_user(dummy_user))
    user: User = dummy_user  # dao.fetch_all_users()[0]
    service: YahooSearchService = YahooSearchService()
    """
    Simplest way to run an async function
    - asyncio.run creates an event loop
    - runs the function
    - brings it down
    
    Pro:
    - Easy to run, you dont have to explicitly create the event loop
    
    Con
    - the event loop it creates is not re-usable, only available for itself
    """
    response: SearchResults = asyncio.run(
        service.yahoo_search(user.user_id, search_term)
    )
    print(response)
