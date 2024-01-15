"""
Make an API call service to google. The service should include keywords input into the encoded url which will then
make a call via google search, passing in the keywords as query parameters for example:
https://google.com/search?q=menstrual+cycle+how+long

Include production level details such as logging, exceptions on top of your service.
"""

from urllib.parse import quote # This method url-encodes a string, allowing it to be passed into a url
import logging # logging library
from typing import Any
import requests
from retry import retry

""" CONCEPT 1"""
# Initialise the logger, create a logger object first:
logger: logging.Logger = logging.Logger(__name__)
# Set the desired level of your logging
logger.setLevel(logging.INFO)

""" CONCEPT 2"""
#FileHandle -> this is use to print the logs like a typical print() function
#The purpose to using this is to allow logs are sent into a file. Logs are like history stamps of what happened during execution
#The log management system then reads the file which contains the logs
#For non-production, we can use a streamhandler instead of a filehandler

file_handler = logging.FileHandler("google_search.logs")
file_handler.setLevel(logging.INFO)

""" CONCEPT 3"""
#Setting up the logging formatter -> to format the logs with timestamp, name, level of logging, message
formatter: logging.Formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
#Tell the logger to pass its log to the file handler
logger.addHandler(file_handler)



# 1) Creating the API Service (Define a method that helps us to create a URL
def __create_url(search_term: str):
    # We use the double underscore here to indicate to python that this is a private method, which means that the
    # function is only available in this file or module.

    return f"https://www.google.com/search?q={quote(search_term)}"

# 2) Making the API call after you have your compatible url string done up.
@retry(exceptions=requests.exception.HTTPError, tries=5, delay=1, jitter=(-0.1,0.1))
def google_search(search_term: str) -> str | None:
    """
    Errors you may run into when making an API call:
    1) HTTPError: eg wifi goes down -> Log and retry if it raises the HTTPError
    2) Status 200: ok
    Status 400: Client side (us) fucked up
    Status 500: Server error (google) fucked up
    """
    # Create a logger to log the error:
    logger.error(f"Started google_search for {search_term}")
    try:
        url: str = __create_url(search_term)
        response: requests.Response = requests.get(url)
    except requests.exceptions.HTTPError as e:
        logger.error(e)
        raise e

    if response.status_code == 200:
        return response.text
    else:
        logger.error(f"Response has a non 200 status code: {response.status_code} for url: {url}")
        return None

if __name__ == "__main__":
    search_term: str = "menstrual cycle"
    response: str = google_search(search_term)

