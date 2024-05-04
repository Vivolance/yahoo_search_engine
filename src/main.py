from typing import Any

from aiohttp import web
from src.models.search_results import SearchResults
from src.models.user import User
from src.services.yahoo_search_dao import YahooSearchDAO
from src.services.yahoo_search_service import YahooSearchService
from dotenv import load_dotenv

"""
We are setting up an asynchronous server
This server is responsible for exposing
the ability to query google search + persist it in our database

our users will call our endpoint with a search term

In this first step, we will setup a dummy route first
to pulse check that aiohttp's server works

We will then, build on top, to expose our GoogleSearchService class to the server

"""

# load environment variables from .env file in root
load_dotenv()
app: web.Application = web.Application()
dao: YahooSearchDAO = YahooSearchDAO()
search_engine: YahooSearchService = YahooSearchService(yahoo_search_dao=dao)


async def hello_world_handle(request: web.Request) -> web.Response:
    """
    web.Request is a dictionary-like class
    """
    return web.Response(text="Hello World")


async def search_yahoo_handle(request: web.Request) -> web.Response:
    """
    web.Request is a dictionary-like class
    """
    data_from_user: dict[str, Any] = await request.json()
    try:
        search_query: str = data_from_user["query"]
        user_id: str = data_from_user["user_id"]
    except KeyError as e:
        return web.json_response(
            data={"error": f"user_id and query not provided: {e}"}, status=400
        )
    try:
        result: SearchResults = await search_engine.yahoo_search(
            user_id=user_id, search_term=search_query
        )
    except Exception as e:
        return web.json_response(
            data={"error": f"Server ran into error: {e}"}, status=500
        )

    final_result: dict[str, Any] = result.model_dump()
    final_result["created_at"] = final_result["created_at"].strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    return web.json_response(data=final_result)


async def create_user_handle(request: web.Request) -> web.Response:
    try:
        user: User = User.create_user()
        await dao.insert_user(user)
    except Exception as e:
        return web.json_response(
            data={"error": f"Server ran into error: {e}"}, status=500
        )
    final_result: dict[str, Any] = user.model_dump()
    final_result["created_at"] = final_result["created_at"].strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    return web.json_response(data=final_result)


"""   
Defines the routes the users can hit
"""
app.add_routes(
    [
        web.get("/hello_world", hello_world_handle),
        web.post("/search", search_yahoo_handle),
        web.post("/create_user", create_user_handle),
    ]
)

if __name__ == "__main__":
    """
    We must set the host to be 0.0.0.0, to allow the python server
    in the docker container to accept connections outside
    of the docker container / virtual machine

    If it is localhost, it won't accept it
    """
    web.run_app(app, host="0.0.0.0", port=8080)
