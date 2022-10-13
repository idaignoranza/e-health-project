def classify(article_list):
    import re
    import numpy as np

    import nltk
    nltk.download("stopwords")
    sw = nltk.corpus.stopwords.words('english')

    abstract_list = [None for _ in range(len(article_list))]
    count_list = [None for _ in range(len(article_list))]
    i = 0
    for art in article_list:
        count=[]
        if art.abstract != None:
            ab = art.abstract.lower()  # metto l'abstract minuscolo
            ab = re.sub(r'[.,"\'?:!;_]', '', ab)  # per rimuovere punteggiatura
            ab_v = ab.split()
            ab_v1 = []
            for word in ab_v:
                if word not in sw:
                    ab_v1.append(word)
            abstract_list[i] = ab_v1

            for j in range(0, len(ab_v1)):
                if ab_v1[j] in ab:
                    count.append(ab.count(ab_v1[j]))

            count_list[i]=count
            i = i + 1
    #word_freq=[]
    #word_freq = [abstract_list[0].count(p) for p in abstract_list[0]]
    #print(word_freq)
    print(abstract_list[0])
    print(count_list[0])
    print(abstract_list[1])
    print(count_list[1])
