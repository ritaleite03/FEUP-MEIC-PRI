import wikipediaapi
import sys
sys.path.append('../../')
from utils import load_json, save_json
from bs4 import BeautifulSoup
import requests
import re
from concurrent.futures import ThreadPoolExecutor

def get_full_info(section):
    full_info = {}
    full_info["Summary"] = section.text.strip().replace("\n", " ")
    for subsection in section.sections:
        full_info[subsection.title] = subsection.text.strip().replace("\n", " ")
    return full_info

def get_row_info(row):
    info = re.sub(r'\[\d+\]', '', row.find('td').text.strip().replace("\n", " "))
    return info.replace(';', ',')

def get_row_list(row):
    content = re.sub(r"(,\s+(and|or))\s+", ",", row)
    return [info.strip()[0].upper() + info.strip()[1:] for info in content.split(",") if info.strip()]


def get_wikipedia_revision_info(page_title):
    # URL to get the last revision date (rvlimit=1 gives the latest one)
    url_last_revision = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={page_title}&rvlimit=1&rvprop=timestamp&format=json"
    
    # URL to get all revisions (rvprop=ids for only revision IDs)
    url_total_revisions = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={page_title}&rvlimit=max&rvprop=ids&format=json"
    
    try:
        last_revision_response = requests.get(url_last_revision).json()
        page_info = next(iter(last_revision_response['query']['pages'].values()))
        
        # Verifica se existem revisões
        if 'revisions' in page_info and len(page_info['revisions']) > 0:
            last_revision_date = page_info['revisions'][0]['timestamp']
        else:
            last_revision_date = None
            print(f"No revisions found for page: {page_title}")
        
        # Tentar obter o número total de revisões
        total_revisions_response = requests.get(url_total_revisions).json()
        total_revisions = len(total_revisions_response['query']['pages'][str(page_info['pageid'])]['revisions'])
    
    except (KeyError, IndexError, requests.exceptions.RequestException) as e:
        # Tratar qualquer erro que ocorra (ex: página não existe, ou problema na requisição)
        print(f"Error retrieving revision info for page: {page_title} - {e}")
        total_revisions = 0
        last_revision_date = None
    
    return total_revisions, last_revision_date


def get_disease_info(disease_page):   
    disease_info = {}

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = f"https://en.wikipedia.org/wiki/{disease_page.title}"
    session = requests.Session()
    session.get('https://www.wikipedia.org', headers=headers)
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Request error for {url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'infobox'})

    if table:
        rows = table.findAll('tr')

        for row in rows:
            if row.find('th') and row.find('th').text == "Other names":
                td = row.find('td')
                if td: 
                    spec = re.sub(r"(,?\s+(and|or|;))\s+", ",", get_row_info(row))
                    disease_info["Alias"] = [s.strip().capitalize() for s in spec.split(",") if s.strip()]
            elif row.find('th') and row.find('th').text == "Specialty":
                td = row.find('td')
                if td:
                    info = get_row_info(row)
                    disease_info["Specialty"] = [s.strip().capitalize() for s in info.split("," ) if s.strip()]
            elif row.find('th') and row.find('th').text == "Symptoms":
                td = row.find('td')
                if td:
                    info = get_row_info(row)
                    disease_info["Symptoms List"] = get_row_list(info)

            elif row.find('th') and row.find('th').text == "Causes":
                td = row.find('td')
                if td:
                    info = get_row_info(row)
                    disease_info["Caused By"] =  get_row_list(info)

            elif row.find('th') and row.find('th').text == "Treatment":
                td = row.find('td')
                if td:
                    info = get_row_info(row)
                    disease_info["Treatments List"] =  get_row_list(info)

            elif row.find('th') and row.find('th').text == "Prevention":
                td = row.find('td')
                if td:
                    full_info = {}
                    full_info["Summary"] = get_row_info(row)
                    disease_info["Prevention"] = full_info

            elif row.find('th') and row.find('th').text == "Risk factors":
                td = row.find('td')
                if td:
                    info = get_row_info(row)
                    disease_info["Risk Factors List"] =  get_row_list(info)

            elif row.find('th') and row.find('th').text == "Complications":
                td = row.find('td')
                if td:
                    full_info = {}
                    full_info["Summary"] = get_row_info(row)
                    disease_info["Complications"] = full_info
 
    disease_info["Overview"] = disease_page.summary.strip().replace("\n", " ")

    for section in disease_page.sections:
        if section.text.strip() == "":
            continue;
        elif section.title == "Signs and symptoms":
            disease_info["Symptoms"] = get_full_info(section)
        elif section.title == "Causes":
            disease_info["Causes"] = get_full_info(section)
        elif section.title == "Diagnosis":
            disease_info["Diagnosis"] = get_full_info(section)
        elif section.title == "Treatment":
            disease_info["Treatment"] = get_full_info(section)
        elif section.title == "Prevention":
            disease_info["Prevention"] = get_full_info(section)
        elif section.title == "Risk factors":
            disease_info["Risk factors"] = get_full_info(section)
        elif section.title == "Complications":
            disease_info["Complications"] = get_full_info(section)

    disease_info["Total Revisions"], disease_info["Last Revision Date"] = get_wikipedia_revision_info(disease_page.title)

    return disease_info

def process_disease(key, wiki_wiki):
    
    page = wiki_wiki.page(f"{key}")
    if not page.exists():
        print(f"Page not found! - {key}")
        return None, None
    else:
        print(f"{key} - Page found!")
        return page.title, get_disease_info(page)

def main(file, endfile, wiki_wiki):
    data = load_json(file)
    all_diseases = {}

    i = 0
    with ThreadPoolExecutor() as executor:
        # Submit tasks to the thread pool and retrieve results
        futures = [executor.submit(process_disease, key, wiki_wiki) for key in data.keys()]
        
        for future in futures:
            title, info = future.result()  # Waits for each thread to complete
            if title and info:
                i += 1
                all_diseases[title] = info

    print(f"Diseases on wikidata: {len(data)}")
    print(f"Diseases on wikipedia and wikidata: {i}")
    print(f"Real Diseases on wikipedia and wikidata: {len(all_diseases)}")
    save_json(endfile, all_diseases)

if __name__ == "__main__":
    file = "../wikidata.json"
    endfile = "wikipedia_from_wikidata.json"

    wiki_wiki = wikipediaapi.Wikipedia('PRI-Proj', 'en')
    main(file, endfile, wiki_wiki)