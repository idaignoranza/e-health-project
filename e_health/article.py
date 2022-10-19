from typing import List, Dict, Optional
import re


class Article:
    """A single document."""

    title: Optional[str]
    authors: Optional[str]
    doi: Optional[str]
    pubmed_id: Optional[str]
    abstract: Optional[str]
    pub_date: Optional[str]
    researchkeys: Optional[str]
    score: Optional[str]

    def __init__(
        self,
        title: str,
        doi: str,
        pubmed_id: str,
        abstract: str,
        pub_date: str,
        authors: List[Dict] or str,
        researchkeys: str,
        score: str,
    ):

        if title == "":
            self.title = None
        else:
            self.title = title

        if doi is not None:
            self.doi = doi.split()[0]
        else:
            self.doi = None

        if pubmed_id is not None:
            self.pubmed_id = pubmed_id.split()[0]
        else:
            self.pubmed_id = None

        if abstract == "":
            self.abstract = None
        else:
            self.abstract = abstract

        if pub_date == "":
            self.pub_date = None
        else:
            self.pub_date = pub_date

        if isinstance(authors, str):
            self.authors = authors
        else:
            # Join authors into a string
            self.authors = ""
            authors_len = len(authors)
            for i, auth in enumerate(authors):
                first_name = auth["firstname"]
                last_name = auth["lastname"]
                if (
                    last_name is not None
                    and last_name != ""
                    and first_name is not None
                    and first_name != ""
                ):
                    self.authors = self.authors + first_name + " " + last_name
                    if (i + 1) < authors_len:
                        self.authors = self.authors + ", "

        if researchkeys == "":
            self.researchkeys = None
        else:
            self.researchkeys = researchkeys
        if score == "":
            self.score = None
        else:
            self.score = score


    # Count how many times the given word `word` appears in the abstract;
    # return 0 if the article has no abstract.
    def count_in_abstract(self, word: str):

        if self.abstract is None:
            return 0

        # lowercase the abstract
        abstract = self.abstract.lower()

        # remove punctuation
        abstract = re.sub(r'[.,"\'?:!;_-]', " ", abstract)

        count = self.abstract.count(word)
        # print("article", self.title, "contains", word, "in abs", count, "times")
        return count

    # Count how many times the given word `word` appears in the title;
    # return 0 if the article has no title.
    def count_in_title(self, word: str):

        if self.title is None:
            return 0

        # lowercase the title
        title = self.title.lower()

        # remove punctuation
        title = re.sub(r'[.,"\'?:!;_-]', " ", title)

        count = title.count(word)
        # print("article", self.title, "contains", word, "in title", count, "times")
        return count

    def get_keys(self):
        if self.researchkeys is None:
            return []

        keys = self.researchkeys.lower()
        keys = re.sub(r'[.,"\'?:!;_(){}]', "", keys)
        keys = keys.split()
        return keys

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"(title: {self.title}, authors: {self.authors}, doi: {self.doi}, pubmed_id: {self.pubmed_id}, abstract: {self.abstract}, pub_date: {self.pub_date}, researchkeys: {self.researchkeys}, score: {self.score}"
