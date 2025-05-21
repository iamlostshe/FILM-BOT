"""Database module."""

import sqlite3

from film_bot.models import Anime, Dorama


def create_tables(db_connection: sqlite3.connect) -> None:
    """Create tables."""
    cursor = db_connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS doramas (chat_id INTEGER,name TEXT,comment TEXT)",
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS anime (chat_id INTEGER,",
        "name TEXT,",
        "comment TEXT)",
    )
    db_connection.commit()


def load_user_data(db_connection: sqlite3.connect) -> dict:
    """Load users data."""
    user_data = {}

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM doramas")
    doramas = cursor.fetchall()
    cursor.execute("SELECT * FROM anime")
    anime = cursor.fetchall()

    for chat_id, name, comments in doramas:
        user_data[chat_id]["doramas"].append(Dorama(name, comments))

    for chat_id, name, comments in anime:
        user_data[chat_id]["anime"].append(Anime(name, comments))

    return user_data
