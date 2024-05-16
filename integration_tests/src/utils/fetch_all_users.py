from src.models.user import User
from sqlalchemy import TextClause, text

from integration_tests.src.utils.engine import engine

class FetchUsers:

    @staticmethod
    async def fetch_users() -> list[User]:
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