#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pymed import PubMed
import e_health


# # Connect to the database

# In[2]:


db_path = "data/db"
db = e_health.db.DBManager(db_path)
print("Connecting to", db_path)


# In[3]:


# Check if table and database exists
if os.path.exists(db_path) and db.check_exists():
    db.clear_table()
    print("cleared existing db")
else:
    db.create_table()


# # Fetch articles

# In[4]:
pubmed = PubMed()
print("----------")
sel=input("Insert the term that you want to find: ")
num=input("Insert how many articles do you want to find: ")
results = pubmed.query(sel, max_results=int(num))
print("----------")

#pubmed = PubMed()
#results = pubmed.query(query, max_results=max_results)


# # Populate the database

# In[5]:


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

    print('\n----------------\n')
    print("made article:", "\ntitle:", article.title,
                          "\npubmed id:", article.pubmed_id,
                          "\ndoi:", article.doi,
                          "\ndate:", article.pub_date,
                          "\nauthors:", article.authors
                          )
    articles.append(article)

db.insert_documents_and_commit(articles)


# In[6]:

print("db contains", len(db.get_articles()), "articles")




