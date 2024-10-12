import requests
import json
from bs4 import BeautifulSoup
from string import ascii_uppercase

VALID_KEYS = ['Overview', 'Symptoms', 'Causes', 'Risk factors', 'Complications', 'Prevention', 'Treatment', 'Diagnosis']

def get_diseases_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        names_divs = soup.find_all('div', class_='cmp-result-name')
        names = []
        for div in names_divs:
            link = div.find('a')
            if link:
                names.append((link.text.strip(), link['href'])) 
        return names
    print("Error in get_diseases_url")
    return []

def get_second_url(soup):
    anchor = soup.find("a", attrs={"id":"et_genericNavigation_diagnosis-treatment"})
    if anchor:
        return "https://www.mayoclinic.org" +  anchor['href']
    else:
        li = soup.find("li", attrs={"data-active":"false"})
        if li:
            return "https://www.mayoclinic.org" + li.find("a")['href']
    return None

def get_first_page_info(disease: str, url: str, headers, session):
    try:
        session.get('https://www.mayoclinic.org', headers=headers)        
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            second_url = get_second_url(soup)
            
            content_div = soup.find('div', class_='content')
            headers = {'Overview': "", 'Symptoms': "", 'Causes': "", 'Risk factors': "", 'Complications': "", 'Prevention': ""}
            if content_div:
                first_div = None
                for child in content_div.findChildren(recursive=False):
                    if child.name == 'div' and not child.has_attr('class'):
                        first_div = child
                        break
                content_div = first_div     
                if content_div is not None:         
                    elements = content_div.find_all(['h2', 'h3'])
                    for h2 in elements:
                        h2_text = h2.text.strip()
                        content_between = []
                        for sibling in h2.find_next_siblings():
                            if sibling.name == 'h2':
                                break
                            if sibling.name in ['p', 'ul']:
                                content_between.append(sibling.text.strip())
                        if disease == h2_text:
                            h2_text = 'Overview'
                        headers[h2_text] = " ".join(content_between).replace('\n', ' ')
                    return headers, second_url
                else:
                    print(f"Error finding the first_div of the disease {disease}")
                    return None
            else:
                section_names = {'overview': 'Overview', 'symptoms': 'Symptoms', 'causes': 'Causes', 'risk-factors': 'Risk factors', 'complications': 'Complications', 'prevention': 'Prevention'}
                for name, title in section_names.items():
                    section = soup.find('section', {'aria-labelledby': name})
                    if section is None:
                        print(f"Error finding section {name} of the disease {disease}")
                    else:
                        section_text = section.find('div', class_='cmp-text__rich-content').get_text(separator=' ', strip=True)
                        headers[title] = section_text
                return headers, second_url
        else:
            print(f"Error accessing the URL: {url} of the disease {disease} - Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None

# apenas para a funcao 'get_second_page_info'
def get_section_information(section):
    text = ""
    section_content = section.findChild(recursive=False)
    for child in section_content.findChildren(recursive=False)[1:]:
        text += child.text.replace('\n', ' ').strip() + " "
    return text

def get_second_page_info(url, headers, session):
    info = {'Diagnosis': "", 'Treatment': ""}

    if url is None:
        return info

    try:
        session.get('https://www.mayoclinic.org', headers=headers)
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            reference_div = soup.find('div', attrs={'class':'content'})

            if reference_div:
                content_div = reference_div.findChild('div', attrs={'class':None})
                formatted_text = ""

                for child in content_div.findChildren(recursive=False):
                    if child.text == "Diagnosis":
                        continue

                    if child.text == "Treatment":
                        info['Diagnosis'] = formatted_text
                        formatted_text = ""
                        continue

                    child_classes = child.get("class")

                    if child_classes and any((True for class_ in child_classes if class_ in ['mc-callout', 'acces-list-container', 'rc-list', 'access-modal', 'video', 'EmbedVideo'])):
                        continue

                    if child_classes and any((True for class_ in child_classes if class_ in ['thin-content-by', 'requestappt'])):
                        info['Treatment'] = formatted_text
                        break

                    formatted_text += child.text.strip().replace('\n', ' ') + " "

                return info
            
            else:
                diagnosis_section = soup.find("section", attrs={"aria-labelledby":"diagnosis"})
                treatment_section = soup.find("section", attrs={"aria-labelledby":"treatment"})

                if diagnosis_section:
                    info['Diagnosis'] = get_section_information(diagnosis_section)
                if treatment_section:
                    info['Treatment'] = get_section_information(treatment_section)

                return info

    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None
    
    return info

def get_disease_info(disease: str, url: str):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    session = requests.Session() 

    info = {}

    first_page_info, second_url = get_first_page_info(disease, url, headers, session)
    second_page_info = get_second_page_info(second_url, headers, session)

    info.update(first_page_info)
    info.update(second_page_info)

    return info

all_diseases_url = []

for letter in ascii_uppercase:
    url = f"https://www.mayoclinic.org/diseases-conditions/index?letter={letter}"
    names = get_diseases_url(url)
    all_diseases_url.extend(names)

all_diseases = {}
for disease, url in all_diseases_url:
    disease_info = get_disease_info(disease, url)
    if disease_info:
        disease_info = {key: disease_info[key].strip() for key in disease_info.keys() if key in VALID_KEYS}
        all_diseases[disease] = disease_info


with open('mayo_diseases.json', 'w', encoding='UTF-8') as file:
    json.dump(all_diseases, file, ensure_ascii=False, indent=4)
        
