
import sqlite3
from typing import List

from e_health.article import Article


class DBManager:
    """Manages a DB connection."""

    db_path: str

    # The connection to the database
    # I don't know what type they have, so I can't define them here
    # however, we can define them in __init__ and use them later
    #
    # connection
    # cursor

    def __init__(self, db_path: str):
        self.db_path = db_path
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
        except BaseException as e:
            raise e

    # Delete table. Do nothing if the table does not exists.
    def delete_table(self):
        query_text = "DROP TABLE Articles"
        try:
            self.cursor.execute(query_text)
        except BaseException as e:
            raise e

    # Check if table exists.
    def check_exists(self) -> bool:
        query_text = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Articles'"
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

    # Create an empty table.
    def create_table(self):
        try:
            query_text = (
                "CREATE TABLE Articles ("
                "ID INTEGER PRIMARY KEY AUTOINCREMENT,  PubmedID TEXT, DOI TEXT, Title TEXT, PubDate TEXT, "
                "Authors TEXT, Abstract TEXT, ResearchKeys TEXT)"
            )
            self.cursor.execute(query_text)
        except sqlite3.Error as e:
            raise e

    # Insert a new document into the database. Note: this function DOES NOT commit the query.
    def insert_document(self, doc: Article):
        try:
            query_text = "INSERT INTO Articles (PubmedID, DOI, Title, PubDate, Authors, Abstract, ResearchKeys) VALUES (?,?,?,?,?,?,?)"
            self.cursor.execute(
                query_text,
                [
                    doc.pubmed_id,
                    doc.doi,
                    doc.title,
                    doc.pub_date,
                    doc.authors,
                    doc.abstract,
                    doc.researchkeys,
                ],
            )
        except BaseException as e:
            raise e

    # Insert a list of document into the database and commit.
    def insert_documents_and_commit(self, docs: List[Article]):
        for doc in docs:
            self.insert_document(doc)
        self.connection.commit()

    # Get the list of articles from the database.
    def get_articles(self):
        self.cursor.execute("select * from Articles")
        results = self.cursor.fetchall()
        return list(map(self._art_from_tuple, results))

    def _art_from_tuple(self, t):
        (_, pubmed_id, doi, title, pub_date, authors, abstract, researchkeys) = t
        return Article(
            title=title,
            pubmed_id=pubmed_id,
            doi=doi,
            abstract=abstract,
            pub_date=pub_date,
            authors=authors,
            researchkeys=researchkeys,
        )

    # Close the database.
    def close(self):
        self.cursor.close()
        self.connection.close()