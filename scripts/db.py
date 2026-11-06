"""Shared PostgreSQL settings; passwords are never stored in source code."""

import os
from getpass import getpass

from sqlalchemy import URL, create_engine


def create_db_engine():
    user = os.environ.get("PGUSER", "postgres")
    password = os.environ.get("PGPASSWORD")
    if password is None:
        password = getpass(f"PostgreSQL password for {user}: ")

    url = URL.create(
        drivername="postgresql+psycopg",
        username=user,
        password=password,
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", "5432")),
        database=os.environ.get("PGDATABASE", "bank_churn"),
    )
    return create_engine(url, connect_args={"connect_timeout": 5})
