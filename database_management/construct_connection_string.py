import os


def construct_sqlalchemy_url() -> str:
    url_tokens: dict[str, str] = {
        "DB_USER": os.getenv("DB_USER", ""),
        "DB_PASSWORD": os.getenv("DB_PASSWORD", ""),
        "DB_HOST": os.getenv("DB_HOST", ""),
        "DB_DATABASE": os.getenv("DB_DATABASE", ""),
        "DB_PORT": os.getenv("DB_PORT", ""),
    }
    url: str = f"postgresql://{url_tokens['DB_USER']}:{url_tokens['DB_PASSWORD']}@{url_tokens['DB_HOST']}:{url_tokens['DB_PORT']}/{url_tokens['DB_DATABASE']}"
    return url
