import wikipediaapi
import json
from bs4 import BeautifulSoup
import requests
from string import ascii_uppercase
import re

def get_wikipedia_revision_info(page_title):
    # URL to get the last revision date (rvlimit=1 gives the latest one)
    url_last_revision = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={page_title}&rvlimit=1&rvprop=timestamp&format=json"
    
    # URL to get all revisions (rvprop=ids for only revision IDs)
    url_total_revisions = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={page_title}&rvlimit=max&rvprop=ids&format=json"
    
    # Get the last revision date
    last_revision_response = requests.get(url_last_revision).json()
    page_info = next(iter(last_revision_response['query']['pages'].values()))
    last_revision_date = page_info['revisions'][0]['timestamp']
    
    # Get the total number of revisions
    total_revisions_response = requests.get(url_total_revisions).json()
    total_revisions = len(total_revisions_response['query']['pages'][str(page_info['pageid'])]['revisions'])

    return total_revisions, last_revision_date

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
                spec = re.sub(r"(,?\s+(and|or|;))\s+", ",", get_row_info(row))
                disease_info["Alias"] = [s.strip().capitalize() for s in spec.split(",") if s.strip()]
            elif row.find('th') and row.find('th').text == "Specialty":
                info = get_row_info(row)
                disease_info["Specialty"] = [s.strip().capitalize() for s in info.split("," ) if s.strip()]
            elif row.find('th') and row.find('th').text == "Symptoms":
                info = get_row_info(row)
                disease_info["Symptoms List"] = get_row_list(info)

            elif row.find('th') and row.find('th').text == "Causes":
                info = get_row_info(row)
                disease_info["Caused By"] =  get_row_list(info)

            elif row.find('th') and row.find('th').text == "Treatment":
                info = get_row_info(row)
                disease_info["Treatments List"] =  get_row_list(info)

            elif row.find('th') and row.find('th').text == "Prevention":
                full_info = {}
                full_info["Summary"] = get_row_info(row)
                disease_info["Prevention"] = full_info

            elif row.find('th') and row.find('th').text == "Risk factors":
                info = get_row_info(row)
                disease_info["Risk Factors List"] =  get_row_list(info)

            elif row.find('th') and row.find('th').text == "Complications":
                full_info = {}
                full_info["Summary"] = get_row_info(row)
                disease_info["Complications"] = full_info
 
    disease_info["Overview"] = disease_page.summary.strip().replace("\n", " ")

    for section in disease_page.sections:
        if section.text.strip() == "":
            continue
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


wiki_wiki = wikipediaapi.Wikipedia('PRI-Proj', 'en')

all_diseases = {}
for letter in ascii_uppercase:
    page = wiki_wiki.page(f"List_of_diseases_({letter})")

    if not page.exists():
        print("Page not found!")
    
    else:
        for link, page in page.links.items():
            if link.startswith("List of") or link.startswith("Outline of"):
                continue
            if not page.exists():
                print("Disease not found: " + link)
                continue
            all_diseases[page.title] = get_disease_info(page)

with open('raw_data/wikipedia_new.json', 'w', encoding='UTF-8') as file:
    json.dump(all_diseases, file, ensure_ascii=False, indent=4)
            
