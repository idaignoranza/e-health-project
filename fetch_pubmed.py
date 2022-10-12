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
                            "\nresearchkeys:", article.researchkeys
                           )

    duplicate = 0

    # Controllo duplicati:
    for x in list:
        if x.doi == result.doi:
            # questa funzione non funziona (vedi db)
            # db.update_task((sel))
            duplicate = 1


    if duplicate == 0:
        # append article:
        articles.append(article)


db.insert_documents_and_commit(articles)


print('\n----------------\n')
print("db contains", len(db.get_articles()), "articles")


# ------------ SECONDA PARTE ---------------

# contiamo quante volte compaiono le parole chiave

article_list = db.get_articles()

keyword_list1 = ['kid','kids','child','children','infant','baby','babies','infants','childhood']
keyword_list2 = ['serious game','serious games','serious video games','serious video game','serious videogames','serious videogame']
keyword_list3 = ['adhd','attention deficit hyperactivity disorder','cognitive','cognitive disorder','cognitive disorders']

import re

count_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
count_list2 = [0, 0, 0, 0, 0, 0]
count_list3 = [0, 0, 0, 0, 0]

for art in article_list:
    if art.abstract != None:
        ab = art.abstract.lower() #metto l'abstract minuscolo
        ab = re.sub(r'[.,"\'?:!;]', '', ab)  # per rimuovere punteggiatura

        for i in range(0, len(keyword_list1)):
            if keyword_list1[i] in ab:
                count_list1[i] = ab.count(keyword_list1[i])

        for j in range(0, len(keyword_list2)):
            if keyword_list2[j] in ab:
                count_list2[j] = ab.count(keyword_list2[j])

        for k in range(0, len(keyword_list3)):
            if keyword_list3[k] in ab:
                count_list3[k] = ab.count(keyword_list3[k])


        if sum(count_list1)>0 and sum(count_list2)>0 and sum(count_list3)>0:
            print('RELEVANT ARTICLE (',art.title,')')

count_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
count_list2 = [0, 0, 0, 0, 0, 0]
count_list3 = [0, 0, 0, 0, 0]

db.close()
