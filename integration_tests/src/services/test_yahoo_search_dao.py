from datetime import datetime
from uuid import UUID
import pytest
from sqlalchemy import TextClause, text

from conftest import integration_test_db_config

from src.models.search_results import SearchResults
from src.models.user import User
from src.services.yahoo_search_dao import YahooSearchDAO

dummy_uuid: UUID = UUID("12345678123456781234567812345678")
# Initialize service here,
# to reuse it across all tests here
# We can't define this as a fixture class scope,
# as it will clash with other pytest fixtures of e.g function scope
yahoo_search_dao: YahooSearchDAO = YahooSearchDAO(integration_test_db_config())


class TestYahooSearchDAO:
    """
    We use pytest-asyncio-cooperative
    - https://stackoverflow.com/questions/74257916/pytest-asyncio-run-multiple-tests-gives-error-regarding-event-loop

    So that we use one event loop for all tests

    Run the tests with pytest-asyncio OFF and sequential
    running of tests ON (ie. --max-asyncio-tasks 1):
    pytest -p no:asyncio --max-asyncio-tasks 1

    This ensures, our tests are running one by one
    - Both tests here truncates the same table
    - They should not run together; they can cause each other to fail
    """

    async def clear_user_table(self) -> None:
        """
        Runs at the start of every integration test
        - Truncate users table
        """
        truncate_clause: TextClause = text("TRUNCATE TABLE users CASCADE")
        async with yahoo_search_dao._engine.begin() as connection:
            await connection.execute(truncate_clause)

    async def clear_search_table(self) -> None:
        """
        Runs at the start of every integration test
        - Truncate search results table
        """
        truncate_clause: TextClause = text("TRUNCATE TABLE search_results")
        async with yahoo_search_dao._engine.begin() as connection:
            await connection.execute(truncate_clause)

    # Allows all your async tests to run on the same event loop
    # Why? -> Impt for IT on database because you do not want to have 2 test
    # to run in parallel to interfere with the same table
    @pytest.mark.asyncio_cooperative
    async def test_insert_user(self) -> None:
        await self.clear_user_table()
        users: list[User] = [
            User(
                user_id=str(dummy_uuid),
                created_at=datetime(year=2024, month=4, day=10, hour=12),
            )
        ]
        for user in users:
            await yahoo_search_dao.insert_user(user)
        """
        Over here, this integration test technically tests for two functions
        - insert + fetch
        - this isn't ideal, as the test should be focused on insert_user
        
        A better way would be to duplicate the fetch_all_users function
        into an integration test utility folder
        
        However, for simplicity and since this is a mini project
        we decided to just go with this, for simplicity
        """
        results_row: list[User] = await yahoo_search_dao.fetch_all_users()
        assert results_row == users
        await self.clear_user_table()

    @pytest.mark.asyncio_cooperative
    async def test_insert_search(self) -> None:
        await self.clear_search_table()
        await self.clear_user_table()
        users: list[User] = [
            User(
                user_id=str(dummy_uuid),
                created_at=datetime(year=2024, month=4, day=10, hour=12),
            )
        ]
        for user in users:
            await yahoo_search_dao.insert_user(user)

        search_results: list[SearchResults] = [
            SearchResults(
                search_id="dummy_search_id",
                user_id=str(dummy_uuid),
                search_term="coffee bean tea leaf",
                result="dummy results",
                created_at=datetime(year=2024, month=4, day=10, hour=12),
            )
        ]
        for search_result in search_results:
            await yahoo_search_dao.insert_search(search_result)

        """
        Over here, this integration test technically tests for two functions
        - insert + fetch
        - this isn't ideal, as the test should be focused on insert_search

        A better way would be to duplicate the fetch_all_users function
        into an integration test utility folder

        However, for simplicity and since this is a mini project
        we decided to just go with this, for simplicity
        """
        results_row: list[SearchResults] = await yahoo_search_dao.fetch_all_searches()
        assert results_row == search_results
        await self.clear_search_table()
        await self.clear_user_table()
