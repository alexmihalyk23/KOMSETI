import requests
from bs4 import BeautifulSoup
import csv

# Функция для получения данных о гитарах на одной странице
def parse_guitars(url, writer):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    guitars = soup.find_all(class_="showcase-item-3")
    for guitar in guitars:
        name = guitar.find(class_="showcase-name-first").text
        description = guitar.find(class_="showcase-name-second").text
        code = guitar.find(class_="product-code").text
        price = guitar.find(itemprop="price")['content']
        currency = guitar.find(itemprop="priceCurrency")['content']
        writer.writerow([name, description, code, price, currency])

# Основная функция для парсинга
def parse_all_guitars_to_csv():
    print("Идет парсинг страницы Мир Музыки...")
    base_url = 'https://mirm.ru/catalog/gitari/elektrogitari/'
    page = 1
    with open('guitars_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Описание', 'Артикул', 'Цена', 'Валюта'])
        while page != 60:
            url = f'{base_url}?PAGEN_1={page}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            guitars = soup.find_all(class_="showcase-item-3")
            if not guitars:
                break
            parse_guitars(url, writer)
            page += 1

parse_all_guitars_to_csv()
