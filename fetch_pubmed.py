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
                            "\nresearchkeys:", article.researchkeys
                           )

    #for db.get_articles().doi in db.get_articles():
        #if result.doi == db.get_articles().doi:
           # db.get_articles().researchkeys.append(article.researchkeys),
           # break


    # append article:
    articles.append(article)

db.insert_documents_and_commit(articles)

print('\n----------------\n')
print("db contains", len(db.get_articles()), "articles")

db.close()