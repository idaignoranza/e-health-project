#!/usr/bin/env python
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

# This holds the count of keywords appearances in the abstract (per article)
abs_counts = {}

# This holds the count of keywords appearances in the title (per article)
title_counts = {}

#    --------- this one is the index of the article in the list
#    |   +---- this one is the article itself
#    v   v
for art in articles:
    # get the 'cleaned-up' keys... (see definition in article.py)
    keys = art.get_keys()

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
    abs_counts[art.pubmed_id] = [art.count_in_abstract(k) for k in keys]
    title_counts[art.pubmed_id] = [art.count_in_title(k) for k in keys]

# Inserire qui, se necessario, stampe di vario genere...
value_ab = {pid: float(sum(abs_count)) for (pid, abs_count) in abs_counts.items()}

#                   +------------+ note that sum([]) = 0
#                   |            | so there's no need to check if tit_count is None,
#                   v            v as we initialized it to []...
value_tit = {
    pid: (float(sum(tit_count)) * 0.75) for (pid, tit_count) in title_counts.items()
}

# Somma gli elementi degli score per abstract e titolo
count_sums = {}
for article in articles:
    pid = article.pubmed_id
    count_sums[pid] = float(value_ab[pid] + value_tit[pid])

score = {}
thresholds = np.linspace(0, 1, num=21)
score_bin = {t: {} for t in thresholds}

min_count = min(count_sums.values())
max_count = max(count_sums.values())

for (pid, count) in count_sums.items():
    val = (count - min_count) / (max_count - min_count)
    score[pid] = val

    for t in thresholds:
        if val <= t:
            score_bin[t][pid] = 0
        elif val > t:
            score_bin[t][pid] = 1

sens = {}  # sensitivity dictionary
spec = {}  # specificity dictionary

manual_scores_df = pd.read_csv("strings.csv")

if manual_scores_df is None:
    print("errore!!!!")
    quit()

assert manual_scores_df is not None

manual_scores_df = manual_scores_df.fillna(0)
manual_scores = {str(p.pubmed_id) : p.Score1 for p in manual_scores_df.itertuples()}

for (t, articles_score) in score_bin.items():

    count_TP = 0
    count_TN = 0
    count_FP = 0
    count_FN = 0

    for (pid, score) in articles_score.items():
        # Ottieni il valore contenuto in strings.csv per il pid `pid`
        manual_score = manual_scores.get(pid)

        if manual_score is None: 
            continue

        if manual_score == 1 and score == 1:
            count_TP += 1
        elif manual_score == 1 and score == 0:
            count_FN += 1
        elif manual_score == 0 and score == 1:
            count_FP += 1
        elif manual_score == 0 and score == 0:
            count_TN += 1

    if (count_TP == 0 and count_FN == 0) or (count_TN == 0 and count_FP == 0): 
        print("Cannot compute sensitivity and specificity for threshold", t)
        continue

    sens[t] = float(count_TP) / float(count_TP + count_FN)
    spec[t] = float(count_TN) / float(count_TN + count_FP)

    print("Specificity for threshold [", t, "] is", spec[t])
    print("Sensitivity for threshold [", t, "] is", sens[t])
    print("-------------")

db.close()
# 1)  (attention AND (disorder OR disorders)) OR "ADHD") AND (serious AND (game OR games))
# 2)  ((attention AND (disorder OR disorders)) OR "ADHD") AND (kid OR kids OR child OR children OR childhood) AND (treatment OR treatments OR therapy OR therapies) NOT (adult OR adults)
# 3)  ((attention AND (disorder OR disorders)) OR "ADHD") AND ((computer AND (game OR games)) OR (game-based)) AND (therapy OR therapies OR treatment OR treatments)
