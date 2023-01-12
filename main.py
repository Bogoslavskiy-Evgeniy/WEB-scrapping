import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
from pprint import pprint

HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

def get_headers():
    return(Headers(browser='chrome', os='win').generate())

hh_main_html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(hh_main_html, features='lxml')
vacancy_list_tag = soup.find('div', class_='vacancy-serp-content')
vacancy_tags = vacancy_list_tag.find_all('div', class_='serp-item')
vacancy_list = []
for vacancy in vacancy_tags:
    # description = vac.find('div', class_='g-user-content').text
    link = vacancy.find('a', class_='serp-item__title')['href']
    vacancy_text = requests.get(link, headers=get_headers()).text
    soup2 = BeautifulSoup(vacancy_text, features='lxml')
    description = soup2.find('div', class_='vacancy-description').stripped_strings
    description_text = [text for text in description]
    if 'Dgango' and 'Flask' in description_text:
        link = vacancy.find('a', class_='serp-item__title')['href']
        company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text
        city_address = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
        city = city_address.split(',')[0]
        salary = soup2.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text

        vacancy_list.append({
            'link': link,
            'salary': salary.replace(u"\xa0", " "),
            'company': company.replace(u"\xa0", " "),
            'city': city
        })
pprint(vacancy_list)

with open('vacancy.json', 'w') as f:
    json.dump(vacancy_list, f, ensure_ascii=False, indent=2)
