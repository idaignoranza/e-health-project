#!/usr/bin/env python
# coding: utf-8


import os
from pymed import PubMed
import e_health
#import pandas as pd

# # Connect to the database

db_path = "data/data.db"
db = e_health.db.DBManager(db_path)
print("Connecting to", db_path)


# Check if table and database exists
if os.path.exists(db_path) and db.check_exists():
    db.clear_table()
    print("cleared existing db")
else:
    db.create_table()


# # Fetch articles

pubmed = PubMed()
print("----------")
sel=input("Insert the term that you want to find: ")
num=input("Insert how many articles do you want to find: ")
results = pubmed.query(sel, max_results=int(num))
print("----------")

#pubmed = PubMed()
#results = pubmed.query(query, max_results=max_results)


# # Populate the database

articles = []

for result in results:
    title = result.title
    pid = result.pubmed_id
    doi = result.doi
    abstract = result.abstract
    pub_date = result.publication_date 
    authors = result.authors
    
    
    # print("got article with title", title, "pid", pid, "doi", doi, "abstract", abstract, "pub_date", pub_date, "authors", authors)
    article = e_health.article.Article(title = title, pubmed_id=pid, 
                                             doi = doi, abstract = abstract,
                                             pub_date = pub_date, authors = authors )

    # print article:
    print('\n----------------\n')
    print("made article:", "\ntitle:", article.title,
                           "\npubmed id:", article.pubmed_id,
                           "\ndoi:", article.doi,
                           "\ndate:", article.pub_date,
                           "\nauthors:", article.authors
                           )

    # append article:
    articles.append(article)


db.insert_documents_and_commit(articles)

print('\n----------------\n')
print("db contains", len(db.get_articles()), "articles")

db.close()