import datetime
import uuid

from pydantic import BaseModel


class SearchResults(BaseModel):
    search_id: str
    user_id: str
    search_term: str
    result: str | None
    created_at: str

    @staticmethod
    def create(user_id: str, search_term: str, result: str | None) -> "SearchResults":
        return SearchResults(
            search_id=str(uuid.uuid4()),
            user_id=user_id,
            search_term=search_term,
            result=result,
            created_at=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        )
