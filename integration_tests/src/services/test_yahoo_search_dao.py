from datetime import datetime
import pytest

from integration_tests.conftest import integration_test_db_config
from integration_tests.src.utils.clear_tables import ClearTables
from integration_tests.src.utils.engine import dummy_uuid
from integration_tests.src.utils.fetch import Fetch

from src.models.search_results import SearchResults
from src.models.user import User
from src.services.yahoo_search_dao import YahooSearchDAO

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

    # Allows all your async tests to run on the same event loop
    # Why? -> Impt for IT on database because you do not want to have 2 test
    # to run in parallel to interfere with the same table
    @pytest.mark.asyncio_cooperative
    async def test_insert_user(self) -> None:
        await ClearTables.clear_user_table()
        users: list[User] = [
            User(
                user_id=str(dummy_uuid),
                created_at=datetime(year=2024, month=4, day=10, hour=12),
            )
        ]
        for user in users:
            await yahoo_search_dao.insert_user(user)

        from integration_tests.src.utils.fetch import Fetch

        results_row: list[User] = await Fetch.fetch_all_users()
        assert results_row == users
        await ClearTables.clear_user_table()

    @pytest.mark.asyncio_cooperative
    async def test_insert_search(self) -> None:
        await ClearTables.clear_search_table()
        await ClearTables.clear_user_table()
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

        results_row: list[SearchResults] = await Fetch.fetch_all_searches()
        assert results_row == search_results
        await ClearTables.clear_search_table()
        await ClearTables.clear_user_table()
