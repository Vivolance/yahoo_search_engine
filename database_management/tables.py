"""
## (Don't do this yet) Users table
- user_id -> uuid.uuid4() -> give you a unique identifier for a user
- created_at -> datetime -> indicates the time the user was created

## (Search Results)
- search_id -> uuid.uuid4() -> unique identifier
- user_id -> (Let's omit this for now)
- search_term -> str (not nullable)
- result -> str | None (google search engine can fail)
- created_at -> datetime (the time the search occurred)
"""
from sqlalchemy import Table, MetaData, String, Column, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
main_metadata: MetaData = MetaData()

user_table: Table = Table(
    "users",
    main_metadata,
    Column("user_id", String, primary_key=True),
    Column("created_at", DateTime, nullable=False)
)

search_results_table = Table(
    "search_results",
    main_metadata,
    Column("search_id", String, primary_key=True),
    Column(
        "user_id",
        String,
        ForeignKey("users.user_id", name="search_results_user_id_to_users_user_id_fk"),
        nullable=True
    ),
    Column("search_term", String, nullable=False),
    Column("result", String, nullable=True),
    Column("created_at", DateTime, nullable=False),
)
