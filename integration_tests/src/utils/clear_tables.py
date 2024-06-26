from sqlalchemy import TextClause, text

from integration_tests.src.utils.engine import engine


class ClearTables:
    @staticmethod
    async def clear_user_table() -> None:
        """
        Runs at the start of every integration test
        - Truncate users table
        """
        truncate_clause: TextClause = text("TRUNCATE TABLE users CASCADE")
        async with engine.begin() as connection:
            await connection.execute(truncate_clause)

    @staticmethod
    async def clear_search_table() -> None:
        """
        Runs at the start of every integration test
        - Truncate search results table
        """
        truncate_clause: TextClause = text("TRUNCATE TABLE search_results")
        async with engine.begin() as connection:
            await connection.execute(truncate_clause)
