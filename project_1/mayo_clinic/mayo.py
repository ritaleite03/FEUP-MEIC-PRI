import requests
from bs4 import BeautifulSoup
import csv

def get_diseases_url(url : str):
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

def get_diseases_info(disease : str, url : str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    session = requests.Session() 
    try:
        session.get('https://www.mayoclinic.org', headers=headers)        
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')            
            content_div = soup.find('div', class_='content')
            headers = {'Overview':"", 'Symptoms':"",'Causes':"",'Risk factors':"",'Complications':"",'Prevention':""}
            if content_div:
                # find div where content is           
                first_div = None
                for child in content_div.findChildren(recursive=False):
                    if child.name == 'div' and not child.has_attr('class'):
                        first_div = child
                        break
                content_div = first_div     
                if content_div is not None:         
                    # find headers and its info
                    elements = content_div.find_all(['h2', 'h3'])
                    for h2 in elements:
                        h2_text = h2.text.strip()
                        content_between = []
                        for sibling in h2.find_next_siblings():
                            if sibling.name == 'h2':
                                break
                            if sibling.name in ['p', 'ul']:
                                content_between.append(sibling.text.strip())
                        # if header is diseases' name then probably there is no Overview
                        if disease == h2_text:
                            h2_text = 'Overview'
                        headers[h2_text] = " ".join(content_between).replace('\n', ' ')
                    return headers
                else:
                    print(f"Erro ao encontrar o first_div of the disease {disease}")
                    return None
                
            # page with different structure
            else:
                section_names = {'overview' : 'Overview', 'symptoms' : 'Symptoms', 'causes' : 'Causes', 'risk-factors' : 'Risk factors', 'complications' : 'Complications', 'prevention' : 'Prevention'}
                for name, title in section_names.items():
                    section = soup.find('section', {'aria-labelledby': name})
                    if section is None:
                        print(f"Erro ao encontrar section {name} of the disease {disease}")
                    else:
                        section_text = section.find('div', class_='cmp-text__rich-content').get_text(separator=' ', strip=True)
                        headers[title] = section_text
                return headers
        else:
            print(f"Erro ao acessar a URL: {url} of the disease {disease} - Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Erro ao fazer requisição para {url}: {e}")
        return None

all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_diseases_url = []

for letter in all_letters:
    url = f"https://www.mayoclinic.org/diseases-conditions/index?letter={letter}"
    names = get_diseases_url(url)
    all_diseases_url.extend(names)
    
#with open('diseases_url.csv', 'w', newline='', encoding='utf-8') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerow(['Name', 'URL'])
#    writer.writerows(all_diseases_url)


with open('diseases_info.csv', 'w', newline='', encoding='utf-8') as result_file:
    writer = csv.writer(result_file)
    writer.writerow(['Name', 'Overview', 'Symptoms', 'Causes', 'Risk factors', 'Complications', 'Prevention'])
    for disease, url in all_diseases_url:
        disease_info = get_diseases_info(disease,url)
        if disease_info:
            writer.writerow([disease, disease_info['Overview'], disease_info['Symptoms'], disease_info['Causes'], disease_info['Risk factors'], disease_info['Complications'], disease_info['Prevention']])
