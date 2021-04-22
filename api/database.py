from __future__ import annotations
import sqlite3
from typing import List, Optional
from api.models.course import Course
from api.models.search_data import SearchData


class Database(object):
    """Object-Relational Mapping class for working with SQLite3 DB."""

    def __init__(
            self,
            file: str=''
        ) -> None:
        """Create a database connection to the SQLite database.
        :param file: the SQLite database file path
        :type file: str
        """
        if file.strip() == '':
            from api import app
            file = app.config["DATABASE"]
        self._conn = sqlite3.connect(file)
        self._cur = self._conn.cursor()
        self.create_table()

    def create_table(self) -> None:
        """Create new table in the database."""
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
        except sqlite3.Error:
            pass

    def get(self, id: int) -> Optional[Course]:
        """Get course information by ID in database.
        :param id: the ID of the training course in the database
        :type id: int
        :return: the detailed information about training course
        :rtype: Optional[Course]
        """
        if id is None or id<0:
            return None
        query = "SELECT * FROM courses WHERE id=?"
        try:
            self._cur.execute(query, (id,))
            record = self._cur.fetchone()
        except sqlite3.Error as e:
            print(e)
        if record:
            return Course(
                name=record[1],
                start=record[2],
                end=record[3],
                amount=record[4],
                id=record[0]
            )
        return

    def add(self, course: Optional[Course]) -> Optional[Course]:
        """Add a training course to the database.
        :param course: the detailed information about training course
        :type course: Optional[Course]
        :return: the course with real ID if it was added successfully
        :rtype: Optional[Course]
        """
        if course is None:
            return
        query = "INSERT INTO courses (name, start, end, amount) VALUES (?,?,?,?)"
        try:
            self._cur.execute(query, (course.name, course.start.isoformat(), course.end.isoformat(), course.amount))
            course.id = self._cur.lastrowid or -1
            self._conn.commit()
        except sqlite3.Error as e:
            print(e)
            return
        return course

    def remove(self, id: int) -> Optional[Course]:
        """Delete a course by ID in the database.
        :param id: the ID of the training course
        :type id: int
        :return: the deleted training course object
        :rtype: Optional[Course]
        """
        if id <= 0:
            return
        query = "DELETE FROM courses WHERE id=?"
        course = self.get(id)
        try:
            self._cur.execute(query, (id,))
            self._conn.commit()
        except sqlite3.Error as e:
            print(e)
            return
        return course

    def update(self, id: int, course: Optional[Course]) -> Optional[Course]:
        """Update the course details stored by the specified ID.
        :param id: the ID of the training course in the database
        :type id: int
        :param course: new course data to update in the database
        :type course: Optional[Course]
        :return: the updated course information
        :rtype: Optional[Course]
        """
        if id is None or id <= 0 or course is None:
            return
        if self.get(id) is None:
            return self.add(course)
        query = "UPDATE courses SET name=?, start=?, end=?, amount=? WHERE id=?"
        try:
            self._cur.execute(query, (course.name, course.start.isoformat(), course.end.isoformat(), course.amount, id))
            self._conn.commit()
        except sqlite3.Error as e:
            print(e)
            return
        course.id = id
        return course

    def search(self, data: Optional[SearchData]=None) -> List[Course]:
        """Search for courses that match the query data.
        :param data: the search query data
        :type data: Optional[SearchData]
        :return: the list of courses that match the search query
        :rtype: List[Course]
        """
        if data is None:
            data = SearchData()
        query = """SELECT * FROM courses
            WHERE instr(name, ?) AND start >= ? AND end <= ?
            ORDER BY start ASC, name ASC"""
        try:
            self._cur.execute(query, (
                    data.name or "",
                    data.start or "1970-01-01",
                    data.end or "9999-12-31"
                )
            )
            records = self._cur.fetchall()
        except sqlite3.Error as e:
            print(e)
        return [Course(
                name=rec[1],
                start=rec[2],
                end=rec[3],
                amount=rec[4],
                id=rec[0]
            ) for rec in records]

    def close(self) -> None:
        """Close the database descriptors."""
        self._cur.close()
        if self._conn:
            self._conn.close()

    def __enter__(self) -> Database:
        """Initial endpoint of the context manager."""
        return self

    def __exit__(self, type, value, traceback) -> Optional[bool]:
        """Always called when exiting from the context manager."""
        self.close()
