from collections.abc import Sequence

import toml
from sqlalchemy import CursorResult, Row, TextClause, text
from sqlalchemy.engine import Engine, create_engine
from typing import Any, MutableMapping

from src.models.search_results import SearchResults
from src.models.user import User


class GoogleSearchDAO:
    """
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

    2. Cache the query into google_searches table
    uery DB by search_term,
    date_inserted >= datetime.utcnow() - timedelta(hours=1)

    2. Cache the query into google_searches table
    """

    def __init__(self):
        self.__config: MutableMapping[str, Any] = toml.load("local_config/config.toml")
        self.__db_config: dict[str, Any] = self.__config["database"]
        self._engine: Engine = create_engine(self.connection_string(self.__db_config))

    @staticmethod
    def connection_string(db_config: dict[str, Any]) -> str:
        host: str | None = db_config.get("host", None)
        user: str | None = db_config.get("user", None)
        password: str | None = db_config.get("password", None)
        database: str | None = db_config.get("database", None)
        port: str | None = db_config["port"]
        return (
            f"postgresql://{host}:{port}/{database}"
            if not user and not password
            else f"postgresql://{user}:{password}@{host}:{port}/{database}"
        )

    def fetch_all_searches(self) -> list[SearchResults]:
        with self._engine.begin() as connection:
            text_clause: TextClause = text(
                "SELECT search_id, user_id, "
                "search_term, result, created_at "
                "FROM search_results"
            )
            cursor: CursorResult = connection.execute(text_clause)
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

    def fetch_all_users(self) -> list[User]:
        with self._engine.begin() as connection:
            text_clause: TextClause = text("SELECT user_id, created_at " "FROM users")
            cursor: CursorResult = connection.execute(text_clause)
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
    dao: GoogleSearchDAO = GoogleSearchDAO()
    search_results: list[SearchResults] = dao.fetch_all_searches()
    print(f"fetch_all_searches: {search_results}")
    users: list[User] = dao.fetch_all_users()
    print(f"fetch_all_searches: {users}")
