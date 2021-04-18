import os.path
import sqlite3
from typing import Optional


class Database(object):
    """Object-Relational Mapping class for working with SQLite3."""

    def __init__(self, file: str="courses.sqlite3") -> None:
        """Create a database connection to the SQLite database.
        :param file: the SQLite database file name
        :type file: str
        """
        file = os.path.join(os.path.dirname(__file__), file)
        self._conn = sqlite3.connect(file)
        self._cur = self._conn.cursor()
        try:
            self._cur.execute(
                """CREATE TABLE 'courses' (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    start DATE NOT NULL,
                    end DATE NOT NULL,
                    amount INTEGER NOT NULL
                )"""
            )
        except sqlite3.Error as e:
            pass
