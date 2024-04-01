from src.services.google_search_service import GoogleSearchService
import pytest
import requests


class TestGoogleSearchEngine:
    @staticmethod
    @pytest.mark.parametrize(
        ["input", "expected"],
        [
            ["menstrual cycle", "https://www.google.com/search?q=menstrual%20cycle"],
            ["elson chan", "https://www.google.com/search?q=elson%20chan"],
        ],
    )
    def test_create_url(input: str, expected: str):
        actual: str = GoogleSearchService.create_url(input)
        assert actual == expected, "url is not formatted correctly"

    @pytest.fixture
    def google_search_engine(self) -> GoogleSearchService:
        return GoogleSearchService()

    @staticmethod
    def dummy_requests_get(url: str, *args, **kwargs) -> requests.Response:
        mock_response: requests.Response = requests.Response()
        mock_response._content = b"Some content"
        mock_response.status_code = 200
        return mock_response

    # @staticmethod
    # def test_google_search(
    #     monkeypatch: MonkeyPatch, google_search_engine: GoogleSearchService
    # ) -> None:
    #     monkeypatch.setattr(
    #         "src.services.google_search_service.requests.get",
    #         TestGoogleSearchEngine.dummy_requests_get,
    #     )
    #     expected: str = "Some content"
    #     actual: str | None = google_search_engine.google_search("some input")
    #     assert (
    #         actual == expected
    #     ), "GoogleSearchEngine.google_search doesn't handle input as expected"
