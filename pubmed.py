from Bio import Entrez
import json
import pandas as pd


def search(query,retstart=0):
    Entrez.email = 'akuzhiv1@binghmaton.edu'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='20',
                            retmode='xml',
                            retstart=retstart,
                            usehistory='y',
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'akuzhiv1@binghmaton.edu'
    handle = Entrez.efetch(db='pubmed',retmode='xml',id=ids)
    results = Entrez.read(handle)
    return results


if __name__ == '__main__':
    topic = input('Enter topic to search: ') or 'artificial intelligence'
    results = search(topic)
    print(f"Total number of results: {results['Count']}")
    nextPage = 'Y'
    for rec in range(0,int(results['Count']),20):
        if nextPage == 'Y':
            results = search(topic,rec)
            id_list = results['IdList']
            papers = fetch_details(id_list)

            # wri_req = input("Do you wish to locally save the JSON file? (Y/N): ")
            # if wri_req == 'Y':
            #     with open("PubMed_A3.json", 'w') as outfile:
            #         json.dump(papers, outfile)

            df = pd.DataFrame(columns=['Article Title', 'Authors', 'PMID', 'Language', 'Date'])
            for i, paper in enumerate(papers['PubmedArticle']):
                authors = []
                for name in paper['MedlineCitation']['Article']['AuthorList']:
                    authors.append(name['LastName'] + ' ' + name['Initials'] + ' ')
                artDate = paper['MedlineCitation']['DateRevised']['Day'] + '/' + paper['MedlineCitation']['DateRevised'][
                    'Month'] + '/' + paper['MedlineCitation']['DateRevised']['Year']
                dictTemp = {
                    "Article Title": paper['MedlineCitation']['Article']['ArticleTitle'],
                    "Authors": ','.join(authors),
                    "PMID": paper['MedlineCitation']['PMID'],
                    "Language": paper['MedlineCitation']['Article']['Language'],
                    "Date": artDate,
                    "Database": 'PubMed'
                }
                # df = pd.DataFrame(dict, index=[i])
                df.loc[len(df.index)] = dictTemp

            with pd.option_context('display.max_rows', None,
                                   'display.max_columns', None,
                                   'display.precision', 3,
                                   ):
                print(df)

            nextPage = input('Do you want to load the next 20 results?(Y/N): ') or ''