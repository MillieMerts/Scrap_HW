import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json


url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
headers = Headers(browser="chrome", os="win")
headers_data = headers.generate()
r = requests.get(url, headers=headers_data).text
soup = BeautifulSoup(r, "lxml")
vacancys = soup.find_all('div', class_="vacancy-serp-item__layout")

vacancy_list = []

def match(host):
    r = requests.get(host, headers=headers_data).text
    url_soup = BeautifulSoup(r, 'lxml')
    job_descript = url_soup.find(attrs={"data-qa": "vacancy-description"}).text
    if "django" in job_descript.lower() or "flask" in job_descript.lower():
        return True
   
for vacancy in vacancys:
    link = vacancy.find('a', class_='serp-item__title').get('href')
    if match(link):
        company_name = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace("\xa0", " ")
        city = vacancy.find('div', {'data-qa':"vacancy-serp__vacancy-address"}, class_="bloko-text").text
        try:
            salary = vacancy.find('span', class_='bloko-header-section-3').text.replace("\u202f", "")
        except:
            salary = "-" 
        vacancy_list.append([link, company_name, city, salary])

print(vacancy_list)
print(len(vacancy_list))

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(vacancy_list, f, ensure_ascii=False)