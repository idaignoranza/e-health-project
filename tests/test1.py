# CREAZIONE DATABASE PIU CONNESSIONE
import sqlite3

try:
    sqliteConnection = sqlite3.connect('Pubmed_research.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")

# CONNESSIONE A PUBMED, SELEZIONE DELLA STRINGA E RACCOLTA DATI
from pymed import PubMed
pubmed = PubMed(tool="MyTool", email="my@email.address")
a=input("Insert the selected string: ")
results = pubmed.query(a, max_results=3)

for res in results:
    TitleV=res.title
    PubmedIDV=res.pubmed_id
    DOIV=res.doi
    AuthorsV=res.authors
    PublicationDateV=res.publication_date
    AbstractV=res.abstract
    values = [PubmedIDV, DOIV, TitleV, AuthorsV, AbstractV]
    print(values)


# INSERIMENTO DATI PRECEDENTEMENTE RACCOLTI
import sqlite3

try:
    sqliteConnection = sqlite3.connect('Pubmed_research.db')
    sqlite_create_table_query = '''CREATE TABLE PubmedDatabase (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                PubmedID TEXT NOT NULL,
                                DOI TEXT NOT NULL,
                                Title TEXT NOT NULL,
                                Authors TEXT NOT NULL,
                                Abstract TEXT NOT NULL);'''

    sqlite_insert_table_query= '''INSERT INTO PubmedDataBase (
                                PubmedId, DOI, Title, Authors, Abstract)
                                VALUES (?,?,?,?,?)'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    cursor.executemany(sqlite_insert_table_query, values)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")