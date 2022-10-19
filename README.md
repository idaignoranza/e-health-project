# E-Health
## Database e PubMed
Dobbiamo decidere quale database utilizzare (SQLite, MySql...), 
al momento gli esempi che abbiamo usano SQLite.
Una volta scelto il DB da utilizzare, dobbiamo trovare e usare una libreria
python per interfacciarci con esso: seguendo l'uso di SQLite, per ora 
abbiamo sempre usato la libreria `sqlite3`. 

Dobbiamo inserire i documenti estratti da PubMed nel database, pertanto
dobbiamo creare una tabella all'interno di quest'ultimo: i dati che
scarichiamo da PubMed tramite la libreria `pymed` hanno la seguente forma: 
```
documento {
     pubmed_id
     title,
     abstract,
     keywords,
     journal,
     publication_date,
     authors,
     methods,
     conclusions,
     results,
     copyrights,
     doi,
     xml,
}
```
Dobbiamo capire:
1. Quali campi (doi, autori, abstract...) di un documento ci interessano 
2. Come modellare la tabella all'interno del database, ossia quali tipi 
corrispondono ai campi e quali chiavi utilizzare (probabilmente un id 
incrementale a partire da `0`?)