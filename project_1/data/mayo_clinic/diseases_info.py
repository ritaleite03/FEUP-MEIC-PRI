import requests
from bs4 import BeautifulSoup

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

def get_diseases_info(disease: str, url: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    session = requests.Session() 
    try:
        session.get('https://www.mayoclinic.org', headers=headers)        
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')            
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
                    return headers
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
                return headers
        else:
            print(f"Error accessing the URL: {url} of the disease {disease} - Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None

def clean_value(value):
    if not value or value.strip() == "":
        return "NULL"
    escaped_value = value.replace("'", "''")
    return f"'{escaped_value}'"

all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_diseases_url = []

for letter in all_letters:
    url = f"https://www.mayoclinic.org/diseases-conditions/index?letter={letter}"
    names = get_diseases_url(url)
    all_diseases_url.extend(names)

with open('diseases_info.sql', 'w', encoding='utf-8') as sql_file:
    sql_file.write('''DROP TABLE IF EXISTS diseases;\n\n''')
    
    sql_file.write('''CREATE TABLE diseases (
        name TEXT PRIMARY KEY,
        overview TEXT,
        symptoms TEXT,
        causes TEXT,
        risk_factors TEXT,
        complications TEXT,
        prevention TEXT
    );\n\n''')

    for disease, url in all_diseases_url:
        disease_info = get_diseases_info(disease, url)
        if disease_info:
            insert_command = f'''INSERT INTO diseases (name, overview, symptoms, causes, risk_factors, complications, prevention) 
            VALUES (
                '{disease.replace("'", "''")}', 
                {clean_value(disease_info['Overview'])}, 
                {clean_value(disease_info['Symptoms'])}, 
                {clean_value(disease_info['Causes'])}, 
                {clean_value(disease_info['Risk factors'])}, 
                {clean_value(disease_info['Complications'])}, 
                {clean_value(disease_info['Prevention'])}
            );\n'''
            sql_file.write(insert_command)

