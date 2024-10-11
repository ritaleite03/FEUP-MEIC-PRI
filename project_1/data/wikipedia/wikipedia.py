import wikipediaapi
import json
from bs4 import BeautifulSoup
import requests
from string import ascii_uppercase
import re


def get_full_info(section):
    full_info = {}
    full_info["Summary"] = section.text.strip().replace("\n", " ")
    for subsection in section.sections:
        full_info[subsection.title] = subsection.text.strip().replace("\n", " ")
    return full_info

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
                disease_info["Alias"] = re.sub(r'\[\d+\]', '', row.find('td').text.strip().replace("\n", " "))
            elif row.find('th') and row.find('th').text == "Specialty":
                spec = row.find('td').text.strip().replace("\n", " ")
                disease_info["Specialty"] = [spec.strip() for spec in spec.split(",")]
 
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

    return disease_info


# def extract_diseases_from_section(section):
#
#     disease_list = {}
#
#     # Add disease names from the current section
#     for line in section.text.splitlines():
#         line = line.strip()
#         if line and line != "== Notes ==":  # Add only non-empty lines
#             line = line.split("/")[0].split(",")[0].split(";")[0]
#
#             disease_page = wiki_wiki.page(line)
#
#             if not disease_page.exists():
#                 print("Disease not found: " + line)
#                 continue
#
#             disease_list[disease_page.title] = (get_disease_info(disease_page))
#
#     # Recursively add disease names from subsections
#     for subsection in section.sections:
#         disease_list |= extract_diseases_from_section(subsection)
#
#     return disease_list


wiki_wiki = wikipediaapi.Wikipedia('PRI-Proj', 'en')

all_diseases = {}
for letter in ascii_uppercase:
    page = wiki_wiki.page(f"List_of_diseases_({letter})")

    if not page.exists():
        print("Page not found!")
    
    else:
        # Extract diseases from the main sections
        # for section in page.sections:
        #     all_diseases |= (extract_diseases_from_section(section))

        for link in page.links.keys():
            if link.startswith("List of") or link.startswith("Outline of"):
                continue
            disease_page = wiki_wiki.page(link)
            if not disease_page.exists():
                print("Disease not found: " + link)
                continue
            all_diseases[disease_page.title] = get_disease_info(disease_page)

with open('wikipedia_diseases.json', 'w', encoding='UTF-8') as file:
    json.dump(all_diseases, file, ensure_ascii=False, indent=4)
            
# with open('wikipedia_diseases.json', 'w', encoding='UTF-8') as file:
#     all_diseases = {}
#     all_diseases |= {"Acute myeloid leukemia": get_disease_info(wiki_wiki.page("Acute myeloid leukemia"))}
#     json.dump(all_diseases, file, ensure_ascii=False, indent=4)
