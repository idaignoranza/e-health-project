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

print(list)

#x.title = 'ciuppa'

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

    duplicate = 0

    # Controllo duplicati:
    for x in list:
        print("entrato nel ciclo")
        print(x.doi)

        if x.doi == result.doi:
            print("duplicato trovato")
            print(sel)
            #x.researchkeys.append(sel)
            duplicate = 1

    #print(duplicate)

    if duplicate == 0:
        # append article:
        articles.append(article)


db.insert_documents_and_commit(articles)

# !!!!!
# PROVA:
#db2 = db.get_articles()
#db2.to_csv('db.csv')

#import csv
#with open('data.csv', 'w') as csvfile:
    #writer = csv.writer(csvfile)
    #writer.writerows(data)


print('\n----------------\n')
print("db contains", len(db.get_articles()), "articles")

# contiamo quante volte compaiono le parole chiave 

article_list = db.get_articles()
keyword_list = ['kid', 'kids', 'child', 'children', 'infant', 'children', 'baby', 'serious game', 'applied game',
                'game-based', 'game based']

import re

count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for art in article_list:
    if art.abstract != None:
        ab = art.abstract.lower() #metto l'abstract minuscolo
        ab = re.sub(r'[.,"\'?:!;]', '', ab)  # per rimuovere punteggiatura

        for i in range(0, len(keyword_list)):
            if keyword_list[i] in ab:
                count_list[i] = ab.count(keyword_list[i])
        print(count_list)
        count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        print("No abstract")


db.close()

