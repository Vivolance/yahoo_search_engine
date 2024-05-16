from collections.abc import Sequence

from src.models.search_results import SearchResults
from src.models.user import User
from integration_tests.src.utils.engine import engine
from sqlalchemy import CursorResult, Row, TextClause, text

class Fetch:

    @staticmethod
    async def fetch_all_users() -> list[User]:
        async with engine.begin() as connection:
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

    @staticmethod
    async def fetch_all_searches() -> list[SearchResults]:
        async with engine.begin() as connection:
            text_clause: TextClause = text(
                "SELECT search_id, "
                "user_id, "
                "search_term, "
                "result, "
                "created_at " 
                "FROM search_results")
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