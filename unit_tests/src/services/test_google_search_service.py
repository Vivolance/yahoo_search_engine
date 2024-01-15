from src.services.google_search_service import GoogleSearchService
import pytest
from pytest import MonkeyPatch
import requests

class TestGoogleSearchEngine:
    @staticmethod
    @pytest.mark.parametrize(
        ["input", "expected"],
        [
            ["menstrual cycle", "https://www.google.com/search?q=menstrual%20cycle"],
            ["elson chan", "https://www.google.com/search?q=elson%20chan"]
        ]
    )
    def test_create_url(input: str, expected: str):
        actual: str = GoogleSearchService.create_url(input)
        assert actual == expected, "url is not formatted correctly"

    @staticmethod
    @pytest.mark.skip("skip for fun")
    def test_mark_skip():
        assert 1 == 1

    @staticmethod
    def dummy_requests_get(url: str, *args, **kwargs) -> requests.Response:
        mock_response: requests.Response = requests.Response()
        mock_response._content = b"Some content"
        mock_response.status_code = 200
        return mock_response

    #Checking your method is getting the text out form the response correctly and checking the status code.
    @staticmethod
    def test_google_search(monkeypatch: MonkeyPatch):
        monkeypatch.setattr("src.services.google_search_service.requests.get", TestGoogleSearchEngine.dummy_requests_get)
        expected: str = "Some content"
        actual: str = GoogleSearchService.google_search("some input")
        assert actual == expected, "GoogleSearchEngine.google_search doesn't handle input as expected"


