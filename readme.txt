1) Used modules
    + pymed
        "A python library that provides access to PubMed."
        We used this library to fetch the articles.
    + pandas
        "A fast, powerful, flexible and easy to use open source data analysis and manipulation tool."
        We used this in order to easily dump the fetched articles into a CSV file.
    + sqlite3
        The built-in (cpython) library providing an interface to the SQLite C library.

2) Environment
    No particular requirements needed. We used Git (with GitHub) and, for the development, PyCharm or occasionally Jupyter;
    We did not use anaconda, virtualenv or "project managers" such as poetry.

3) Scripts
    We decoupled the access to the DB, the internal representation of articles and the script to concretely fetch them.

    + e_health/article.py
        The internal representation of the article.
        We decided to include in this class the attributes title (str), doi (str), pubmed_id (str), abstract (str), pub_date (str),
        authors (List[Dict] or str), researchkeys (List[str]), score (List[str] or str).
        DA AGGIUSTARE CON LE AGGIUNTE !!!!!!

    + e_health/db.py
        An helper class used to interact with the underlying DB (in particular, we chose sqlite).
        This class includes useful functions to manipulate the db:
        - delete_table: to delete completely the db;
        - check_exists: to check if a table exists;
        - clear_table: to delete everything inside the table but not the table;
        - create_table: to create an empty table;
        - insert_document: to insert a document into the database;
        - insert_documents_and_commit: to insert a list of document into the database and commit;
        - update_task: to update parameters of database;
        - get_articles: to get the list of articles from the database;
        - _art_from_tuple: to get information about the tuples in the database !!!!!!
        - close: to close the database;
        - update_score: to update the parameter "Score" of database at the fist research;
        - update_task_score: to update the parameter "Score" of database.

    + fetch_pubmed.py
        This script is the core of this part of the project.
        Conceptually, the execution follows this line of reasoning:

     +------------------+
     | database exists? |
     +----/--------\----+
         /          \
  no    /            \    yes
       /              \
      /                \
+--------+    yes  +---------+
| create ----------- delete? |
+----\---+         +----/----+
      \                /
       \              /
        \            /
         \          /
          \        /
     +-----------------+
     |   ask keyword   |
     +--------|--------+
              |
              |
      +-------|-------+
      |fetch articles |
      +-------|-------+
              |
              |
 +------------|-----------+
 | insert or append to db |
 +------------|-----------+
              |
              |
              |
       +------|-----+
       |dump to csv |
       +------------+