import logging
from urllib.parse import quote

import requests
from retry import retry

from src.models.search_results import SearchResults
from src.models.user import User
from src.services.google_search_dao import GoogleSearchDAO
from src.utils.logging_utils import setup_logging


class GoogleSearchService:
    def __init__(self) -> None:
        self.__logger: logging.Logger = logging.Logger(__name__)
        self.__google_search_dao: GoogleSearchDAO = GoogleSearchDAO()
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
        return f"https://www.google.com/search?q={quote(search_term)}"

    @retry(
        exceptions=requests.exceptions.HTTPError,
        tries=5,
        delay=0.01,
        jitter=(-0.01, 0.01),
        backoff=2,
    )
    def _google_search(self, user_id: str, search_term: str) -> SearchResults:
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
        self.__logger.error(f"Started google_search for {search_term}")
        try:
            """
            catch the request get
            you can commonly get intermittent wifi errors
            when we do, we get a HTTPError
            """
            url: str = GoogleSearchService.create_url(search_term)
            response: requests.Response = requests.get(url)
        except requests.exceptions.HTTPError as e:
            self.__logger.error(e)
            raise e

        if response.status_code == 200:
            result: str = response.text
            search_result = SearchResults.create(
                user_id=user_id, search_term=search_term, result=result
            )
            return search_result
        else:
            self.__logger.error(
                f"Response has a non-200 status code: "
                f"{response.status_code} for url: {url}"
            )
            return SearchResults.create(
                user_id=user_id, search_term=search_term, result=None
            )

    def google_search(self, user_id: str, search_term: str) -> SearchResults:
        """
        Does two things:
        - Performs the search
        - Persist result into the database
        """
        try:
            result: SearchResults = self._google_search(user_id, search_term)
        except Exception:
            result = SearchResults.create(
                user_id=user_id, search_term=search_term, result=None
            )
        self.__google_search_dao.insert_search(result)
        return result


if __name__ == "__main__":
    search_term: str = "menstrual cycle"
    dao: GoogleSearchDAO = GoogleSearchDAO()
    user: User = dao.fetch_all_users()[0]
    service: GoogleSearchService = GoogleSearchService()
    response: SearchResults = service.google_search(user.user_id, search_term)
    print(response)
