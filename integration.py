import pubmed
import pandas as pd

def pubmeddata(topic,starting=0):
    topic = topic
    results = pubmed.search(topic)
    print(f"Total number of results: {results['Count']}")
    for rec in range(starting, starting+20, 20):
        results = pubmed.search(topic, rec)
        id_list = results['IdList']
        papers = pubmed.fetch_details(id_list)
        df = pd.DataFrame(columns=['ArticleTitle', 'Authors', 'PMID', 'Language', 'Date'])
        for i, paper in enumerate(papers['PubmedArticle']):
            authors = []
            if paper['MedlineCitation']['Article']['AuthorList'] is not None:
                for name in paper['MedlineCitation']['Article']['AuthorList']:
                    authors.append(name['LastName'] + ' ' + name['Initials'] + ' ')
            artDate = paper['MedlineCitation']['DateRevised']['Day'] + '/' + \
                      paper['MedlineCitation']['DateRevised'][
                          'Month'] + '/' + paper['MedlineCitation']['DateRevised']['Year']
            dictTemp = {
                "ArticleTitle": paper['MedlineCitation']['Article']['ArticleTitle'],
                "Authors": ','.join(authors),
                "PMID": paper['MedlineCitation']['PMID'],
                "Language": paper['MedlineCitation']['Article']['Language'],
                "Date": artDate,
                "Database": 'PubMed'
            }
            # df = pd.DataFrame(dict, index=[i])
            df.loc[len(df.index)] = dictTemp

    with pd.option_context('display.max_rows', None,'display.max_columns', None,'display.precision', 3,):
        return df

if __name__ == '__main__':
    page ='Y'
    i=0
    while(page == 'Y'):
        data=pubmeddata('(Ai And ML) OR Healthcare',i)
        print(data)
        i=i+20
        page = input('Do you want to load the next 20 results?(Y/N):')