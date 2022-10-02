#!/usr/bin/env python
import os
from os import abort
from typing import List

from pymed import PubMed
import sqlite3

# Crea il database e la tabella principale

db_path = "../data/db"
sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS PubmedDatabase (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                PubmedID TEXT NOT NULL,
                                DOI TEXT NOT NULL,
                                Title TEXT NOT NULL,
                                Authors TEXT NOT NULL,
                                Abstract TEXT NOT NULL);'''

try:
    sqliteConnection = sqlite3.connect(db_path)
    cursor = sqliteConnection.cursor()
    print("Successfully connected to SQLite in path", db_path)
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

except sqlite3.Error as error:
    print("Error while connecting to sqlite (in path", db_path, "):", error, )
    os.abort()


# Ottieni dati da PubMed

query = "coronavirus"
max_results = 5
pubmed = PubMed()
results = pubmed.query(query, max_results=max_results)
sqlite_insert_table_query = '''INSERT INTO PubmedDataBase (PubmedID, DOI, Title, Authors, Abstract) VALUES (?,?,?,?,?)'''

if sqliteConnection is None or cursor is None:
    print("By now, a connection to the db is necessary. Aborting!")
    abort()

for res in results:
    title = res.title
    pubmed_id = res.pubmed_id
    doi = res.doi
    pub_date = res.publication_date
    abstract = res.abstract
    authors = ""
    for i, auth in enumerate(res.authors):
        authors = authors + auth["firstname"] + " " + auth["lastname"]
        if (i+1) < len(res.authors):
            authors = authors + ", "
    cursor.execute(sqlite_insert_table_query, [pubmed_id, doi, title, authors, abstract])

sqliteConnection.commit()
if sqliteConnection is not None:
    sqliteConnection.close()