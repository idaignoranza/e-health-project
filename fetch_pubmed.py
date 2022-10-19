#!/usr/bin/env python
# coding: utf-8
import os

import pandas as pd
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
    score='-'

    
    
    #print("got article with title", title, "pid", pid, "doi", doi, "abstract", abstract, "pub_date", pub_date, "authors", authors, "researchkeys", sel)
    article = e_health.article.Article(title = title, pubmed_id=pid,
                                             doi = doi, abstract = abstract,
                                             pub_date = pub_date, authors = authors, researchkeys=sel, score='-')


    # print article:
    print('\n----------------\n')
    print("made article:", "\ntitle:", article.title,
                           "\npubmed id:", article.pubmed_id,
                           "\ndoi:", article.doi,
                           "\ndate:", article.pub_date,
                           "\nauthors:", article.authors,
                           "\nabstract:", article.abstract,
                            "\nresearchkeys:", article.researchkeys,
                            "\nscore:", article.score
                           )

    duplicate = 0

    # Controllo duplicati:
    for x in list:
        if x.pubmed_id == result.pubmed_id:
            new_researchkeys = x.researchkeys+', '+sel


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
value_ab=db.count_word_abstract(articles)
print(value_ab)
print('\n----------------\n')
print("Counting the keywords in the title")
value_tit=db.count_word_title(articles)
print(value_tit)
#Somma gli elementi degli score per abstract e titolo
somma_ab_tit=[]
for i in range(0,len(value_ab)):
    somma_ab_tit.append(float(value_ab[i]+value_tit[i]))
score=[]
score_bin=[]
for i in range(0,len(somma_ab_tit)):
    val=(somma_ab_tit[i]-min(somma_ab_tit))/(max(somma_ab_tit)-min(somma_ab_tit))
    score.append(val)
    if score[i]<=0.5:
        score_bin.append(0)
    elif score[i]>0.5:
        score_bin.append(1)

print(score_bin)
i=0
for l in articles:
    db.update_score((score_bin[i],l.pubmed_id))
    for res in results:
        if l.pubmed_id==res.pubmed_id:
            new_score=max(res.score,score_bin[i])
            db.update_task_score((new_score, l.pubmed_id))
    i=i+1

