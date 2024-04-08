from src.services.yahoo_search_service import YahooSearchService
import pytest
import requests


class TestYahooSearchEngine:
    @staticmethod
    @pytest.mark.parametrize(
        ["input", "expected"],
        [
            ["menstrual cycle", "https://sg.search.yahoo.com/search?q=menstrual%20cycle"],
            ["elson chan", "https://sg.search.yahoo.com/search?q=elson%20chan"],
        ],
    )
    def test_create_url(input: str, expected: str):
        actual: str = YahooSearchService.create_url(input)
        assert actual == expected, "url is not formatted correctly"

    @pytest.fixture
    def yahoo_search_engine(self) -> YahooSearchService:
        return YahooSearchService()

    @staticmethod
    def dummy_requests_get(url: str, *args, **kwargs) -> requests.Response:
        mock_response: requests.Response = requests.Response()
        mock_response._content = b"Some content"
        mock_response.status_code = 200
        return mock_response