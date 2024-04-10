from uuid import UUID

import pytest
from freezegun import freeze_time
from unittest.mock import patch
from src.models.search_results import SearchResults
from datetime import datetime

dummy_uuid: UUID = UUID("12345678123456781234567812345678")


class TestSearchResult:
    @pytest.mark.parametrize(
        ["user_id", "search_term", "result", "expected_search_result"],
        [
            [
                "dummy_user_id",
                "coffee bean tea leaf",
                "swedish berry",
                SearchResults(
                    search_id=str(dummy_uuid),
                    user_id="dummy_user_id",
                    search_term="coffee bean tea leaf",
                    result="swedish berry",
                    created_at=datetime(year=2024, month=4, day=10, hour=12),
                ),
            ],
            [
                "dummy_user_id",
                "coffee bean no leaf",
                None,
                SearchResults(
                    search_id=str(dummy_uuid),
                    user_id="dummy_user_id",
                    search_term="coffee bean no leaf",
                    result=None,
                    created_at=datetime(year=2024, month=4, day=10, hour=12),
                ),
            ],
        ],
    )
    def test_create(
        self,
        user_id: str,
        search_term: str,
        result: str | None,
        expected_search_result: SearchResults,
    ) -> None:
        with freeze_time("2024-04-10 12:00:00"), patch(
            "src.models.search_results.uuid.uuid4", return_value=dummy_uuid
        ):
            search_results: SearchResults = SearchResults.create(
                user_id=user_id, search_term=search_term, result=result
            )
            assert search_results == expected_search_result
