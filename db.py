
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
                "Authors TEXT, Abstract TEXT, ResearchKeys TEXT, Score TEXT)"
            )
            self.cursor.execute(query_text)
        except sqlite3.Error as e:
            raise e

    # Insert a new document into the database. Note: this function DOES NOT commit the query.
    def insert_document(self, doc: Article):
        try:
            query_text = "INSERT INTO Articles (PubmedID, DOI, Title, PubDate, Authors, Abstract, ResearchKeys, Score) VALUES (?,?,?,?,?,?,?,?)"
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
                    doc.score,
                ],
            )
        except BaseException as e:
            raise e

    # Insert a list of document into the database and commit.
    def insert_documents_and_commit(self, docs: List[Article]):
        for doc in docs:
            self.insert_document(doc)
        self.connection.commit()


    # Modify parameters of database.
    def update_task(self, task):
#       """
#       update researchkeys of a task
#       :param conn:
#       :param task:
#       :return: project id
#       """

       sql = ''' UPDATE Articles
                 SET ResearchKeys = ?
                 WHERE PubmedID = ?'''

       #cur = self.cursor()
       self.cursor.execute(sql, task)
       #self.commit()


    # Get the list of articles from the database.
    def get_articles(self):
        self.cursor.execute("select * from Articles")
        results = self.cursor.fetchall()
        return list(map(self._art_from_tuple, results))

    def _art_from_tuple(self, t):
        (id_, pubmed_id, doi, title, pub_date, authors, abstract, researchkeys, score) = t
        return Article(
            title=title,
            pubmed_id=pubmed_id,
            doi=doi,
            abstract=abstract,
            pub_date=pub_date,
            authors=authors,
            researchkeys=researchkeys,
            score=score,
        )

    # Close the database.
    def close(self):
        self.cursor.close()
        self.connection.close()

        # Counting of the words in the abstract based on the string
    def count_word_abstract(self, article_list):
        import re
        import numpy as np

        import nltk
        nltk.download("stopwords")
        sw = nltk.corpus.stopwords.words('english')

        abstract_list = [None for _ in range(len(article_list))]
        count_list = [None for _ in range(len(article_list))]
        i = 0
        for art in article_list:
            count = []
            if art.abstract != None:
                ab = art.abstract.lower()  # metto l'abstract minuscolo
                ab = re.sub(r'[.,"\'?:!;_]', '', ab)  # per rimuovere punteggiatura
                ab_v1 = []
                string = art.researchkeys.lower()
                string = re.sub(r'[.,"\'?:!;_(){}]', '', string)
                string = string.split()
                str = []


                for word in string:
                    if word not in sw:
                        str.append(word)

                for k in range(0, len(str)):
                    if str[k] in ab:
                        ab_v1.append(str[k])

                    elif str[k] not in ab:
                        ab_v1.append(str[k])

                    elif ab==None:
                        ab_v1.append(str[k])

                abstract_list[i] = ab_v1

                for j in range(0, len(ab_v1)):
                    if ab_v1[j] in string:
                        count.append(ab.count(ab_v1[j]))

                    elif ab_v1[j] not in string:
                        count.append(0)

                    elif ab==None:
                        ab_v1.append(0)

                count_list[i] = count
                i = i + 1

        for k in range(0, len(abstract_list)):
            print(abstract_list[k])
            print(count_list[k])

        value_ab=[]
        for i in range(0, len(count_list)):
            if count_list[i] != None:
                value=float(sum(count_list[i]))

            else:
                value=0

            value_ab.append(float(value))


        return(value_ab)

    #  Counting of the words in the title based on the string
    def count_word_title(self, article_list):
        import re
        import numpy as np

        import nltk
        nltk.download("stopwords")
        sw = nltk.corpus.stopwords.words('english')

        title_list = [None for _ in range(len(article_list))]
        count_list = [None for _ in range(len(article_list))]
        i = 0
        for art in article_list:
            count = []
            if art.title != None:
                tit = art.title.lower()  # metto l'abstract minuscolo
                tit = re.sub(r'[.,"\'?:!;_]', '', tit)  # per rimuovere punteggiatura
                tit_v1 = []
                string = art.researchkeys.lower()
                string = re.sub(r'[.,"\'?:!;_(){}]', '', string)
                string = string.split()
                str = []

                for word in string:
                    if word not in sw:
                        str.append(word)

                for k in range(0, len(str)):
                    if str[k] in tit:
                        tit_v1.append(str[k])

                    elif str[k] not in tit:
                        tit_v1.append(str[k])

                title_list[i] = tit_v1

                for j in range(0, len(tit_v1)):
                    if tit_v1[j] in string:
                        count.append(tit.count(tit_v1[j]))
                    elif tit_v1[j] not in string:
                        count.append(0)

                count_list[i] = count
                i = i + 1

        for k in range(0, len(title_list)):
            print(title_list[k])
            print(count_list[k])

        value_tit=[]
        for i in range(0, len(count_list)):
            if count_list[i] != None:
                value=float(sum(count_list[i]))* 0.75 #Moltiplica i valori dei singoli articoli per il peso 0.75 perchè consideriamo il titolo

            else:
                value=0

            value_tit.append(float(value))


        return(value_tit)

    def update_score(self, val):
        sql_query=''' UPDATE Articles SET Score = ? WHERE PubmedID = ?'''
        self.cursor.execute(sql_query, val)
        self.connection.commit()
