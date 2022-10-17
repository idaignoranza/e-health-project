#!/usr/bin/env python
# coding: utf-8
import os
from pymed import PubMed
import e_health

# # Connect to the database
db_path = "data/data.db"
db = e_health.db.DBManager(db_path)
print("Connecting to", db_path)


# Check if table and database exists
if os.path.exists(db_path) and db.check_exists():
    reset = input("The database already exists! Do you want to reset it? [Y/n] ")
    if reset.upper() == 'Y':
        db.delete_table()
        db.create_table()
else:
    db.create_table()


# # Fetch articles
pubmed = PubMed()
print("----------")
sel = input("Insert the term that you want to find: ")
# keyboard input
num = input("Insert how many articles do you want to find: ")
results = pubmed.query(sel, max_results=int(num))
print("----------")

# # Populate the database

articles = []
list = db.get_articles()

for result in results:
    title = result.title
    pid = result.pubmed_id
    doi = result.doi
    abstract = result.abstract
    pub_date = result.publication_date 
    authors = result.authors
    researchkeys = sel
    
    
    #print("got article with title", title, "pid", pid, "doi", doi, "abstract", abstract, "pub_date", pub_date, "authors", authors, "researchkeys", sel)
    article = e_health.article.Article(title = title, pubmed_id=pid,
                                             doi = doi, abstract = abstract,
                                             pub_date = pub_date, authors = authors, researchkeys=sel)


    # print article:
    print('\n----------------\n')
    print("made article:", "\ntitle:", article.title,
                           "\npubmed id:", article.pubmed_id,
                           "\ndoi:", article.doi,
                           "\ndate:", article.pub_date,
                           "\nauthors:", article.authors,
                           "\nabstract:", article.abstract,
                            "\nresearchkeys:", article.researchkeys
                           )

    duplicate = 0

    # Controllo duplicati:
    for x in list:
        if x.doi == result.doi:
            new_researchkeys = x.researchkeys+', '+sel
            print(new_researchkeys)


            db.update_task((new_researchkeys, x.pubmed_id))
            duplicate = 1


    if duplicate == 0:
        # append article:
        articles.append(article)


db.insert_documents_and_commit(articles)


print('\n----------------\n')
print("Database contains", len(db.get_articles()), "articles")

# ------------ SECONDA PARTE ---------------

# Contiamo quante volte compaiono le parole chiave sia nell'abstract che nel titolo
print('\n----------------\n')
print("Counting the keywords in the abstract")
db.count_word_abstract(articles)
print('\n----------------\n')
print("Counting the keywords in the title")
db.count_word_title(articles)

db.close()
