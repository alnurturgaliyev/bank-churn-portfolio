
from sqlalchemy import text

from db import create_db_engine

engine = create_db_engine()

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_user")
        ).one()

        print("Connected successfully!")
        print("Database:", result[0])
        print("User:", result[1])
finally:
    engine.dispose()
