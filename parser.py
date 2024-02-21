import requests
from bs4 import BeautifulSoup
import csv


pages = []
def max_ids(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        test = soup.find_all(class_="pagination-wrapper")
        for t in test:
            r = t.find_all('a')
            for link in r:
                # print()
                pages.append(int(link["href"].split('=')[-1]))
        return max(pages)
    except Exception as e:
        return 1
    
    

# Функция для получения данных о гитарах на одной странице
def parse_guitars(url, writer):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    guitars = soup.find_all(class_="showcase-item-3")
    
    # print(pages)
    for guitar in guitars:
        name = guitar.find(class_="showcase-name-first").text
        description = guitar.find(class_="showcase-name-second").text
        code = guitar.find(class_="product-code").text
        price = guitar.find(itemprop="price")['content']
        currency = guitar.find(itemprop="priceCurrency")['content']
        writer.writerow([name, description, code, price, currency])

# Основная функция для парсинга
def parse_all_guitars_to_csv(guitar_type, max_ids):
    print("Идет парсинг страницы...")
    base_url = f'https://mirm.ru{guitar_type}/'

    page = 1
    # print(guitar_type.split("/")[-2])
    name_csv = f'guitars_data_{guitar_type.split("/")[-2]}.csv'
    with open(name_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Описание', 'Артикул', 'Цена', 'Валюта'])
        while page != max_ids+1:
            url = f'{base_url}?PAGEN_1={page}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            guitars = soup.find_all(class_="showcase-item-3")
            if not guitars:
                break
            parse_guitars(url, writer)
            print(f"Парсинг {page} страницы")
            page += 1

# parse_all_guitars_to_csv()

# Отправляем GET-запрос на страницу
response = requests.get('https://mirm.ru/catalog/gitari/')

# Создаем объект BeautifulSoup для парсинга HTML-кода
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все элементы с классом "name-wrapper"
name_wrappers = soup.find_all(class_='name-wrapper')

# Выводим названия ссылок
for id, name_wrapper in enumerate(name_wrappers):
    link = name_wrapper.find('a')
    # print(link["href"])
    print(id,link.text.strip())

guitar_dict = {id: name_wrapper.find('a')["href"] for id, name_wrapper in enumerate(name_wrappers)}
# print(guitar_dict)
type_of_guitar = int(input("Введите id для парсинга: "))

parse_all_guitars_to_csv(guitar_dict[type_of_guitar], max_ids(f'https://mirm.ru{guitar_dict[type_of_guitar]}/'))