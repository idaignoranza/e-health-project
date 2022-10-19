
import sqlite3
from typing import List

from e_health.article import Article


class DBManager_Manual:
    """Manages a DB connection."""

    db_path: str

    # The connection to the database
    # I don't know what type they have, so I can't define them here
    # however, we can define them in __init__ and use them later
    #
    # connection
    # cursor

    # self = puntatore all'oggetto stesso --> riferimento a se stesso

    def __init__(self, db_path: str):
        self.db_path = db_path
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            raise e

    # Delete table. Do nothing if the table does not exists.
    def delete_table(self):
        query_text = "DROP TABLE Manual_Articles"
        try:
            self.cursor.execute(query_text)
        except BaseException as e:
            raise e

    # Check if table exists.
    def check_exists(self) -> bool:
        query_text = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Manual_Articles'"
        # sqlite_master è il tipo
        self.cursor.execute(query_text)
        # if the count is 1, then table exists
        return self.cursor.fetchone()[0] == 1

    # Delete everything from the table.
    def clear_table(self):
        try:
            self.cursor.execute("delete from Articles")
        except BaseException as e:
            raise e

    def create_table(self):
        try:
            query_text = (
                "CREATE TABLE Manual_Articles ("
                "ID INTEGER PRIMARY KEY AUTOINCREMENT,  PubmedID TEXT Score TEXT)"
            )
            self.cursor.execute(query_text)
        except sqlite3.Error as e:
            raise e