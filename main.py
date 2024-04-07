from aiohttp import web

"""
We are setting up an asynchronous server
This server is responsible for exposing
the ability to query google search + persist it in our database

our users will call our endpoint with a search term

In this first step, we will setup a dummy route first
to pulse check that aiohttp's server works

We will then, build on top, to expose our GoogleSearchService class to the server

"""
app: web.Application = web.Application()


async def hello_world_handle(request: web.Request) -> web.Response:
    """
    web.Request is a dictionary-like class
    """
    return web.Response(text="Hello World")


"""
Defines the routes the users can hit
"""
app.add_routes([web.get("/hello_world", hello_world_handle)])

if __name__ == "__main__":
    """
    We must set the host to be 0.0.0.0, to allow the python server
    in the docker container to accept connections outside
    of the docker container / virtual machine

    If it is localhost, it won't accept it
    """
    web.run_app(app, host="0.0.0.0", port=8080)
