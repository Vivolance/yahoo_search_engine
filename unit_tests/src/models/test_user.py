from datetime import datetime
from unittest.mock import patch
from uuid import UUID
from freezegun import freeze_time
import pytest
from src.models.user import User


dummy_uuid: UUID = UUID("12345678123456781234567812345678")


class TestUser:
    @pytest.mark.parametrize(
        ["expected_output"],
        [
            [
                User(
                    user_id=str(dummy_uuid),
                    created_at=datetime(year=2024, month=4, day=9, hour=12),
                )
            ]
        ],
    )
    def test_create_user(self, expected_output: User) -> None:
        with freeze_time("2024-04-09 12:00:00"), patch(
            "src.models.user.uuid.uuid4", return_value=dummy_uuid
        ):
            user: User = User.create_user()
            assert user == expected_output
