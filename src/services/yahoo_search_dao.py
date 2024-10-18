import asyncio
from collections.abc import Sequence

import toml
from retry import retry
from sqlalchemy import CursorResult, Row, TextClause, text
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.models.search_results import SearchResults
from src.models.user import User
from src.utils.construct_connection_string import (
    construct_sqlalchemy_url_from_db_config,
)


class YahooSearchDAO:
    """
    In YahooSearchService, we query the search term against Yahoo's Service
    - However, we can have situations where different users give us the same query

    Use Case 1: Caching Queries, within 1 hour
    - We don't have to make the same query again and again
    - The results will always be the same in the same time-period (1 hour)

    Use Case 2: Allows us to do analytics
    - E.G whats the most common search term
    - E.G who is the user who queries us the most
    - E.G what time period have the most queries

    By using PostgreSQL, we can do the analytics at the database level
    - And the database doesn't have to send all
    rows to the python backend, and do the analytics there
    - Network / data transfer is always the slowest;
    its ~10x slower than even reading from disk
    - Avoid huge data transfer across API / database queries at all cost

    Proposed Caching Control Flow:
    1. Q
    In GoogleSearchService, we query the search term against Google's Service
    - However, we can have situations where different users give us the same query

    Use Case 1: Caching Queries, within 1 hour
    - We don't have to make the same query again and again
    - The results will always be the same in the same time-period (1 hour)

    Use Case 2: Allows us to do analytics
    - E.G whats the most common search term
    - E.G who is the user who queries us the most
    - E.G what time period have the most queries

    By using PostgreSQL, we can do the analytics at the database level
    - And the database doesn't have to send all
    rows to the python backend, and do the analytics there
    - Network / data transfer is always the slowest;
    its ~10x slower than even reading from disk
    - Avoid huge data transfer across API / database queries at all cost

    Caching Control Flow:
    1. Query DB by search_term,
    date_inserted >= datetime.utcnow() - timedelta(hours=1)

    2. Cache the query into yahoo_searches table
    uery DB by search_term,
    date_inserted >= datetime.utcnow() - timedelta(hours=1)

    3. Cache the query into search_results table
    """

    def __init__(
        self,
        db_config: dict[str, Any] = toml.load("local_config/config.toml")["database"],
    ):
        self.__db_config: dict[str, Any] = db_config
        self._engine: AsyncEngine = create_async_engine(
            construct_sqlalchemy_url_from_db_config(self.__db_config, use_async_pg=True)
        )

    @retry(
        exceptions=SQLAlchemyError,
        tries=5,
        delay=0.01,
        jitter=(-0.01, 0.01),
        backoff=2,
    )
    async def insert_search(self, result: SearchResults) -> None:
        """
        TODO: Integration test this
        - Retry unit test -> does it catch the SQLAlchemyError
        """
        async with self._engine.begin() as connection:
            insert_clause: TextClause = text(
                "INSERT into search_results("
                "   search_id, "
                "   user_id, "
                "   search_term, "
                "   result, "
                "   created_at"
                ") values ("
                "   :search_id,"
                "   :user_id,"
                "   :search_term,"
                "   :result,"
                "   :created_at"
                ")"
            )
            # use named-params here to prevent SQL-injection attacks
            await connection.execute(
                insert_clause,
                {
                    "search_id": result.search_id,
                    "user_id": result.user_id,
                    "search_term": result.search_term,
                    "result": result.result,
                    "created_at": result.created_at,
                },
            )

    @retry(
        exceptions=SQLAlchemyError,
        tries=5,
        delay=0.01,
        jitter=(-0.01, 0.01),
        backoff=2,
    )
    async def insert_user(self, user: User) -> None:
        """
        TODO: Integration test this
        """
        async with self._engine.begin() as connection:
            insert_clause: TextClause = text(
                "INSERT into users("
                "   user_id, "
                "   created_at"
                ") values ("
                "   :user_id,"
                "   :created_at"
                ")"
            )
            # use named-params here to prevent SQL-injection attacks
            await connection.execute(
                insert_clause, {"user_id": user.user_id, "created_at": user.created_at}
            )

    @retry(
        exceptions=SQLAlchemyError,
        tries=5,
        delay=0.01,
        jitter=(-0.01, 0.01),
        backoff=2,
    )
    async def fetch_all_searches(self) -> list[SearchResults]:
        """
        Integration test this
        """
        async with self._engine.begin() as connection:
            text_clause: TextClause = text(
                "SELECT search_id, user_id, "
                "search_term, result, created_at "
                "FROM search_results"
            )
            cursor: CursorResult = await connection.execute(text_clause)
            results: Sequence[Row] = cursor.fetchall()
            results_row: list[SearchResults] = [
                SearchResults.parse_obj(
                    {
                        "search_id": curr_row[0],
                        "user_id": curr_row[1],
                        "search_term": curr_row[2],
                        "result": curr_row[3],
                        "created_at": curr_row[4],
                    }
                )
                for curr_row in results
            ]
        return results_row

    @retry(
        exceptions=SQLAlchemyError,
        tries=5,
        delay=0.01,
        jitter=(-0.01, 0.01),
        backoff=2,
    )
    async def fetch_all_users(self) -> list[User]:
        """
        Integration Test
        """
        async with self._engine.begin() as connection:
            text_clause: TextClause = text("SELECT user_id, created_at " "FROM users")
            cursor: CursorResult = await connection.execute(text_clause)
            results: Sequence[Row] = cursor.fetchall()
            results_row: list[User] = [
                User.parse_obj(
                    {
                        "user_id": curr_row[0],
                        "created_at": curr_row[1],
                    }
                )
                for curr_row in results
            ]
        return results_row


if __name__ == "__main__":
    dao: YahooSearchDAO = YahooSearchDAO()
    sample_user: User = User.create_user()
    sample_search_results: SearchResults = SearchResults.create(
        sample_user.user_id, "how to work at macdonalds", "Dummy Search Results"
    )

    event_loop = asyncio.new_event_loop()
    """
    each line here runs asynchronously
    We know it does, as run_until_complete is not awaited, and no Future is returned
    a Future object represents a computation that promises to be completed in the future
    """
    event_loop.run_until_complete(dao.insert_user(sample_user))
    event_loop.run_until_complete(dao.insert_search(sample_search_results))
    search_results: list[SearchResults] = event_loop.run_until_complete(
        dao.fetch_all_searches()
    )
    print(f"fetch_all_searches: {search_results}")
    users: list[User] = event_loop.run_until_complete(dao.fetch_all_users())
    print(f"fetch_all_searches: {users}")
