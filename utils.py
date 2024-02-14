import requests
import json
import os
from datetime import date


def search_all(source, keywords, apikey, number, count=25, date_start=None, date_end=None, 
               get_abstract=True, get_full_text=False, save_to_file=False):
    """
    source: database to search, 'sciencedirect' or 'scopus'
    keywords: Search words separated by '+'
    apikey: apiKey
    number: number of results to return
    count: number of results for each sub-search
    date_start: Year start
    date_end: Year end
    sort: 'coverDate' or 'relevance' 
    get_abstract: bool, whether to get abstract
    get_full_text: bool, whether to get abstract
    save_to_file: bool, whether to save results to file
    """
    results_all = get_all_results(source, keywords, apikey, number, count, date_start, date_end, get_abstract, get_full_text)

    if save_to_file:
        save_results(results_all, source, keywords, number, date_start, date_end)

    return results_all

def get_all_results(source, keywords, apikey, number, count, date_start, date_end, get_abstract, get_full_text):
    results_all = []
    for i in range(int(number / count)):
        search_res = search(source, keywords, apikey, date_start, date_end, start=count*i, count=count, 
                            get_abstract=get_abstract, get_full_text=get_full_text)
        results_all += search_res
    search_res = search(source, keywords, apikey, date_start, date_end, start=count*int(number / count), count=number%count, 
                            get_abstract=get_abstract, get_full_text=get_full_text)
    results_all += search_res
    return results_all

def save_results(results_all, source, keywords, number, date_start=None, date_end=None):
    os.makedirs('files', exist_ok=True)
    name = f"files/{date.today()}_{source}_{keywords}_{number}"
    if date_start != None and date_end != None:
        name += f"_{date_start}_{date_end}"
    with open(f"{name}.json", "w") as outfile: 
        json.dump(results_all, outfile)

def search(source, keywords, apikey, date_start=None, date_end=None, start=0, count=25, sort='relevance', 
           get_abstract=True, get_full_text=False, print_to_screen=False): 
   
    request_full = f"{source}?keywords={keywords}&count={count}&start={start}&sort={sort}"
    if date_start != None and date_end != None:
        request_full += f"&date={date_start}-{date_end}"
    search_response = requests.get(f'https://api.elsevier.com/content/search/{request_full}&apiKey={apikey}')
    try:
        search_results = search_response.json()['search-results']['entry']
    except:
        print(search_response.json())
    
    for r in search_results:
        if get_full_text:
            r['full_text'] = full_text(r['dc:identifier'][4:], apikey)
        if get_abstract:
            r['abstract'] = abstract(r['dc:identifier'][4:], apikey)
        if print_to_screen:
            print_result(r)
    
    return search_results

def abstract(doi, apikey):
    headers={'Accept': 'application/json'}
    Response = requests.get("https://api.elsevier.com/content/abstract/doi/" +
                        f"{doi}?&apiKey={apikey}", headers=headers)
    result = Response.json()
    try:
        ab = result['abstracts-retrieval-response']['coredata']['dc:description']
    except:
        ab = None
    return ab

def full_text(doi, apikey):
    headers={'Accept': 'application/json'}
    Response = requests.get("https://api.elsevier.com/content/article/doi/" +
                        f"{doi}?&apiKey={apikey}", headers=headers)
    result = Response.json()
    try:
        article = result["full-text-retrieval-response"]["originalText"]
    except:
        article = None
    return article

def print_result(r):
    print(r['dc:title'])
    print(r['prism:publicationName'])
    if 'authors' in r.keys():
        try:
            print([a['$'] for a in r['authors']['author']])
        except:
            print(r['authors']['author'])
    print(r['prism:coverDate'])
    print(r['dc:identifier'])
    if 'abstract' in r.keys():
        print('\n')
        print(r['abstract'])
        print('\n')
    if 'full_text' in r.keys():
        print(r['full_text'])
    print('\n')

def load_json(file):
    with open(file, "r") as f:
        data = json.loads(f.read())
    return data

def all_titles(data):
    titles = []
    for d in data:
        titles.append(d['dc:title'])
    return titles
