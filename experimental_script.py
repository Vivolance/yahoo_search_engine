"""
When it comes to experimenting with features, the first thing to do is a prototype. What is the most minial thing to call it a feature, w
What is the most risky part that we need to de risk?

We are creating a class that make an api call to google

Risk: Making an API call.
"""

"""
Create a function that makes an API call to 

https://www.google.com/search?q=menstrual+cycle+how+many+days

Step 0: (One Responsibility - No I/O) Get a search term

Step 1: (One Responsibility - No I/O) Creating the url with the search terms

Step 2: (One Responsibility - I/O) Make an API call with the url from step 1

Step 3: (One Responsibility - No I/O) Parse the response; get only what you need
- The search results (top 10)
"""
# parse is a module (or file)
# package is a folder (with __init__.py in the folder)
# a library is a repository of packages (google_search_engine repo is a library if published)
from urllib.parse import quote  # this method url-encodes a string, so its compatible to be placed into a url
import requests     # an API call library
from typing import Any
import logging  # logging library
from retry import retry  # library to retry functions, typically database calls and api calls


logger: logging.Logger = logging.Logger(__name__)   # create a logger object
# TODO: go through concept of an enum
# enum is a class that defines a set of possible states
logger.setLevel(logging.INFO)   # set the logger to only log stuff that is info and above

# in production, replace this with a filehandler - a streamhandler prints the logs like a typical print()
# we use a filehandler so the logs are sent into the file, then the log management system reads from there
# console_handler = logging.StreamHandler()   # this receives the logs from the logger
# console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("google_search.logs")
file_handler.setLevel(logging.INFO)

# setup the logging formatter, to format the logs with time logged, name, level of the message, and the message itself
formatter: logging.Formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)  # tell the logger to pass its logs to the streamhandler; so it shows up on our console

# reminder: we dont want this in production
# we dont want to show the logs in the service / pods, show for fuck, you also wont see
# arbo send into a file, so you can send it to your log management system
# so we can do complex search queries on the logs on that log management system


def __create_url(search_term: str) -> str:
    """
    a function with 2 __ prefix is private in python
    - this means this function is only available in this file (or module)

    Given a search term e.g "menstrual cycle"
    1. Url encode it -> "menstrual+cycle"
    2. Concatenate the base url "https://www.google.com/search?q=" with step 1
    :param search_term:
    :return:

    Tip: When you want to solve a problem
    Ask yourself if it is likely a common problem other engineers have to solve
    if yes, there is likely an existing library for it - search it
    it derisks the worse case scenario of you creating a feature
    only to realize, it already exists

    TODO: Basic Unit testing
    """
    return f"https://www.google.com/search?q={quote(search_term)}"


@retry(exceptions=requests.exceptions.HTTPError, tries=5, delay=1, jitter=(-0.1, 0.1))
def google_search(search_term: str) -> str | None:
    """
    Makes a request to a google search url
    :param url:
    :return:

    Step 1: Make the API call
    - You can run into HTTPError; eg wifi go down
    - Log and Retry the query if it raises a HTTPError

    Step 2: response succeeded
    - status code is 400 (we as the client fucked up)
    - 200 (success)
    - 500 (server error, the google search engine fucked up)

    Advanced Unit test -> mock the request.get response (test the method under different scenarios)
    """
    logger.error(f"Started google_search for {search_term}")
    try:
        # catch the request get
        # you can commonly get intermittent wifi errors
        # when we do, we get a HTTPError
        """
        You can make higher level functions (google_search) use lower level functions (create_url)
        to make your higher level functions easier to use
        
        here, we construct the url for the user in google_search
        now, the users of the function only has to pass in the search term to make the google api call
        they dont have to call create_url first before calling this function
        """
        url: str = __create_url(search_term)
        response: requests.Response = requests.get(url)
    except requests.exceptions.HTTPError as e:
        """
        Debug -> least dangerous level
        Info -> for logging purposes
        Error -> something blew up
        
        In a log management system, they can filter out the non-important logs
        like debug by setting a log level
        - If log level is set to INFO, only logs INFO and above will be logged
        - debug will be ignored
        
        make it a habit to log the error, so we can send the logs to 
        log management systems e.g datadog, graylog
        - allows you to search logs for debugging
        """
        logger.error(e)
        # raise the exception, to let @retry catch the exception and retry
        # Q: What if we raise an exception retry doesnt catch
        # retry doesn't catch loh, it just jibaboom
        # this is what you want
        # because you don't want to retry on exceptions you shouldnt be getting
        # you can get parsing error -> you got a bug
        raise e

    if response.status_code == 200:
        return response.text
    else:
        logger.error(f"Response has a non-200 status code: {response.status_code} for url: {url}")
        return None


if __name__ == "__main__":
    search_term: str = "menstrual cycle"
    response: str = google_search(search_term)
    # print(response)
