import uuid
import datetime
from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    created_at: datetime

    @staticmethod
    def create_user() -> "User":
        return User(
            user_id=str(uuid.uuid4()),
            created_at=datetime.datetime.utcnow()
        )