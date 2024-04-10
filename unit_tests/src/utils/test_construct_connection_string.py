from typing import Any
from unittest.mock import patch

import pytest

from src.utils.construct_connection_string import (
    _construct_sqlalchemy_url,
    construct_sqlalchemy_url_from_env_vars,
)


class TestConstructSQLAlchemyUrl:
    @pytest.mark.parametrize(
        [
            "user",
            "password",
            "host",
            "database",
            "port",
            "use_async_pg",
            "expected_result",
        ],
        [
            [
                "my_user",
                "my_password",
                "my_host",
                "my_database",
                "5432",
                True,
                "postgresql+asyncpg://my_user:my_password@my_host:5432/my_database",
            ],
            [
                "my_user",
                "my_password",
                "my_host",
                "my_database",
                "5432",
                False,
                "postgresql://my_user:my_password@my_host:5432/my_database",
            ],
            [
                "",
                "",
                "my_host",
                "my_database",
                "5432",
                False,
                "postgresql://my_host:5432/my_database",
            ],
        ],
    )
    def test_construct_sqlalchemy_url(
        self,
        user: str,
        password: str,
        host: str,
        database: str,
        port: str,
        use_async_pg: bool,
        expected_result: str,
    ) -> None:
        actual_string: str = _construct_sqlalchemy_url(
            user=user,
            password=password,
            host=host,
            database=database,
            port=port,
            use_async_pg=use_async_pg,
        )
        assert actual_string == expected_result

    @pytest.mark.parametrize(
        [
            "environment_dictionary",
            "use_async_pg",
            "expected_result",
        ],
        [
            [
                {
                    "DB_USER": "my_user",
                    "DB_PASSWORD": "my_password",
                    "DB_HOST": "my_host",
                    "DB_DATABASE": "my_database",
                    "DB_PORT": "5432",
                },
                True,
                "postgresql+asyncpg://my_user:my_password@my_host:5432/my_database",
            ],
        ],
    )
    def test_construct_sqlalchemy_url_with_env_vars(
        self,
        environment_dictionary: dict[str, Any],
        use_async_pg: bool,
        expected_result: str,
    ) -> None:
        with patch.dict("os.environ", environment_dictionary):
            actual_string: str = construct_sqlalchemy_url_from_env_vars(
                use_async_pg=use_async_pg,
            )
            assert actual_string == expected_result
