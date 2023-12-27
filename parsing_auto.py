import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

lst_auto = []

def parse_auto(num_page: int, region: str, brand: str):
    """Парсиг информации об авто"""
       
    #try:
    car_name = brand.lower()
    url = "https://auto.drom.ru/region{}/{}/{}/".format(
        region, car_name, num_page)
    response = requests.get(url)
    
    #if response.status_code != 404:
    soup = BeautifulSoup(response.text, 'html.parser')
    cars = soup.find_all("a", {"data-ftid": "bulls-list_bull"})

    print(url)

    for car in cars:
        title = car.find("span", {"data-ftid": "bull_title"}).text
        title_pred = title.split(f'{brand} ')[0].split(', ')

        model, year = title_pred[0], title_pred[1]

        desc = car.find(
            "div", {
                "data-ftid": "component_inline-bull-description"
            }).text
        location = car.find("span", {
            "data-ftid": "bull_location"
        }).text

        price = car.find("span", {"data-ftid": "bull_price"}).text
        price = re.sub(r"[^\d,.]", '', price)

        lst_auto.append(
            [region, brand, model, year, desc, location, price])

    return lst_auto

parse_auto('all', '50', 'kia')

print(lst_auto)