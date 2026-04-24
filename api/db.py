import mysql.connector
import os
from dotenv import load_dotenv

# .env lives in api/ alongside this file
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

_db = None

def get_db():
    """Lazily connect to MySQL — only when a route actually needs it."""
    global _db
    try:
        if _db and _db.is_connected():
            return _db
    except Exception:
        pass

    host     = os.getenv("DB_HOST", "localhost")
    user     = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    if not all([user, password, database]):
        raise RuntimeError(
            "\n\n  [DB ERROR] Missing credentials in api/.env\n"
            "  Copy api/.env.example to api/.env and fill in your values.\n"
        )

    _db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        autocommit=False,
        connection_timeout=10,
    )
    return _db
