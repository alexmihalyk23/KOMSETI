import requests
from bs4 import BeautifulSoup
import csv
from flask import Flask
from flask import request
import json
from flask import jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Функция для получения данных о гитарах на одной странице
def parse_guitars(url, guitars_data):

    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    guitars = soup.find_all(class_="showcase-item-3")

    for guitar in guitars:
        name = guitar.find(class_="showcase-name-first").text
        description = guitar.find(class_="showcase-name-second").text
        code = guitar.find(class_="product-code").text
        price = guitar.find(itemprop="price")['content']
        currency = guitar.find(itemprop="priceCurrency")['content']
        guitars_data.append({'Название': name, 'Описание': description, 'Артикул': code, 'Цена': price, 'Валюта': currency})

# Основная функция для парсинга
def parse_all_guitars_to_json(url):
    print("Идет парсинг страницы...")
    base_url = url
    guitars_data = []

    page = 1
    while page != 2:
        url = f'{base_url}?PAGEN_1={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        guitars = soup.find_all(class_="showcase-item-3")
        if not guitars:
            break
        parse_guitars(url, guitars_data)
        print(f"Парсинг {page} страницы")
        page += 1
    return guitars_data

@app.route('/parse', methods=['GET'])
def parse_url():
    url = request.args.get('url')
    data = parse_all_guitars_to_json(url)
    return f"<html><body><h1>JSON данные:</h1><pre>{json.dumps(data, ensure_ascii=False)}</pre></body></html>"


if __name__ == '__main__':
    app.run()
