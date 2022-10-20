#!/#!/usr/bin/env python
# coding: utf-8
import os

import numpy as np
import pandas as pd
from pymed import PubMed
import e_health
import nltk

# Connect to the database
db_path = "data/data.db"
db = e_health.DBManager(db_path)
print("Connecting to", db_path)

# Check if table and database exists
if os.path.exists(db_path) and db.check_exists():
    reset = input("The database already exists! Do you want to reset it? [Y/n] ")
    if reset.upper() == "Y":
        db.delete_table()
        db.create_table()
else:
    db.create_table()

# Fetch articles
pubmed = PubMed()

print("----------")
sel = input("Insert the term that you want to find: ")
num = input("Insert how many articles do you want to find: ")
results = pubmed.query(sel, max_results=int(num))
print("----------")

# Populate the database

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
    score = "-"

    # print("got article with title", title, "pid", pid, "doi", doi, "abstract", abstract, "pub_date", pub_date, "authors", authors, "researchkeys", sel)
    article = e_health.Article(
        title=title,
        pubmed_id=pid,
        doi=doi,
        abstract=abstract,
        pub_date=pub_date,
        authors=authors,
        researchkeys=sel,
        score="-",
    )

    # print article:
    print("\n----------------\n")
    print(
        "made article:",
        "\ntitle:",
        article.title,
        "\npubmed id:",
        article.pubmed_id,
        "\ndoi:",
        article.doi,
        "\ndate:",
        article.pub_date,
        "\nauthors:",
        article.authors,
        "\nabstract:",
        article.abstract,
        "\nresearchkeys:",
        article.researchkeys,
        "\nscore:",
        article.score,
    )

    duplicate = 0

    # Controllo duplicati:
    for x in list:
        if x.pubmed_id == result.pubmed_id:
            new_researchkeys = x.researchkeys + ", " + sel

            db.update_task((new_researchkeys, x.pubmed_id))
            duplicate = 1

    if duplicate == 0:
        # append article:
        articles.append(article)

db.insert_documents_and_commit(articles)

print("\n----------------\n")
print("Database contains", len(db.get_articles()), "articles")


# ------------ CLASSIFICATION ---------------

articles = db.get_articles()

# Count how many times the keywords appear in both the abstract and the title
print("\n----------------\n")

nltk.download("stopwords")
stopwords = nltk.corpus.stopwords.words("english")
print("Counting the keywords in the abstract")

# This holds the list of keywords in each article
keys_list = [[] for _ in articles]

# This holds the count of keywords appearances in the abstract (per article)
abs_count_list = [[] for _ in articles]

# This holds the count of keywords appearances in the title (per article)
title_count_list = [[] for _ in articles]

#    --------- this one is the index of the article in the list
#    |   +---- this one is the article itself
#    v   v
for (i, art) in enumerate(articles):
    # get the 'cleaned-up' keys... (see definition in article.py)
    keys = art.get_keys()

    # initialize keys_list[i] to the list of keys we have just computed
    keys_list[i] = [k for k in keys]

    # (see the definitions of count_in_* in article.py)

    #                   +-- this is called list comprehension -+
    #                   |                         + for every +|
    #                   |                         | key `k`   ||
    #                   |                         | in `keys` ||
    #                   |                         |           ||
    #                   | compute the result of   |           ||
    #                   | art.count_in_abstract(k)|           ||
    #                   |                         |           ||
    #                   v                         v           vv
    abs_count_list[i] = [art.count_in_abstract(k) for k in keys]

    title_count_list[i] = [art.count_in_title(k) for k in keys]

# Inserire qui, se necessario, stampe di vario genere...
value_ab = [float(sum(abs_count)) for abs_count in abs_count_list]
#                   +------------+ note that sum([]) = 0
#                   |            | so there's no need to check if tit_count is None,
#                   v            v as we initialized it to []...
value_tit = [(float(sum(tit_count)) * 0.75) for tit_count in title_count_list]

# Somma gli elementi degli score per abstract e titolo
somma_ab_tit = []
for i in range(0, len(value_ab)):
    somma_ab_tit.append(float(value_ab[i] + value_tit[i]))

# print(somma_ab_tit)
score = []
thresh=np.linspace(0,1,num=21)
score_bin =[[] for _ in thresh ]
for i in range(0, len(somma_ab_tit)):
    val = (somma_ab_tit[i] - min(somma_ab_tit)) / (
        max(somma_ab_tit) - min(somma_ab_tit)
    )
    score.append(val)
    for j in range(0,len(thresh)):
        if score[i] <= thresh[j]:
            score_bin[j].append(0)
        elif score[i] > thresh[j]:
            score_bin[j].append(1)


sens=[None for _ in score_bin]  # sensitivity vector
spec=[None for _ in score_bin]  # specificity vector
for k in range(0, len(score_bin)):
    print('THRESHOLD = ', round(thresh[k],2),'\n')
    print(score_bin[k])
    i = 0

    for l in articles:
        db.update_score((score_bin[k][i], l.pubmed_id))
        #for res in results:
         #   if l.pubmed_id == res.pubmed_id:
          #      new_score = max(res.score, score_bin[k][i])
           #     db.update_task_score((new_score, l.pubmed_id))
        i = i + 1


# Export in csv
    import pandas as pd

    articles = db.get_articles()
    articles_dict = [a.__dict__ for a in articles]
    df = pd.DataFrame(articles_dict)

    df.to_csv("data/data.csv", index=False)

    df=pd.read_csv('data/data.csv', index_col=0)
    #print(df)

    df1=pd.read_csv('strings.csv', index_col=0)
    df1=df1.fillna(0)
    #print(df1)

    df2=df.join(df1, on='pubmed_id', how='inner')#, lsuffix='', rsuffix='', sort=False, validate=None)

    count_TP=0
    count_TN=0
    count_FP=0
    count_FN=0
    ind=[]
    for i in range(0,len(df2.index)):
        ind.append(i)
    df2.index=ind
    #print(df2)

    for i in range(0,len(df2.index)):
        if df2.loc[i]['score']==0 and df2.loc[i]['Score1']==1:
            count_FN=count_FN+1
        elif df2.loc[i]['score']==1 and df2.loc[i]['Score1']==0:
            count_FP = count_FP + 1
        elif df2.loc[i]['score']==1 and df2.loc[i]['Score1']==1:
            count_TP = count_TP + 1
        elif df2.loc[i]['score']==0 and df2.loc[i]['Score1']==0:
            count_TN = count_TN + 1

    #print(count_FN,count_FP,count_TN,count_TP)
    sens[k]=float(count_TP)/float(count_TP+count_FN)
    spec[k]=float(count_TN)/float(count_TN+count_FP)
    print('Specificity=',spec[k])
    print('Sensitivity=',sens[k])
    print("-------------")

db.close()

# 1)  (attention AND (disorder OR disorders)) OR "ADHD") AND (serious AND (game OR games))
# 2)  ((attention AND (disorder OR disorders)) OR "ADHD") AND (kid OR kids OR child OR children OR childhood) AND (treatment OR treatments OR therapy OR therapies) NOT (adult OR adults)
# 3)  ((attention AND (disorder OR disorders)) OR "ADHD") AND ((computer AND (game OR games)) OR (game-based)) AND (therapy OR therapies OR treatment OR treatments)