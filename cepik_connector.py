from datetime import datetime, time
import sys

import requests
from urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import urllib.parse as urlparse
from urllib.parse import parse_qs
import sqlite3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_voivodeship_dictionary():
    voivodeship_dict = dict()
    LINK = 'https://api.cepik.gov.pl/slowniki/wojewodztwa'
    response = requests.get(LINK, verify= False)
    response_json = response.json()
    response_json_data = response_json['data']
    attributes = response_json_data['attributes']['dostepne-rekordy-slownika']
    for att in attributes:
        voivodeship_dict[att['wartosc-slownika']] = att['klucz-slownika']
    return voivodeship_dict


def get_max_pages(voivodship):
    cepik_link = f"https://api.cepik.gov.pl/pojazdy?wojewodztwo={voivodship}&data-od=20200601&data-do=20201201&typ-daty=1" \
                 f"&tylko-zarejestrowane=true&pokaz-wszystkie-pola=false&limit=500"
    response = requests.get(cepik_link, verify=False)
    response_json = response.json()
    parsed = urlparse.urlparse(response_json['links']['last'])
    max_page = int(parse_qs(parsed.query)['page'][0])
    return max_page




def get_cars_dataframe(voivodeships):
    df = pd.DataFrame()
    page_int = 1
    print('Start voivodeships loop')
    for key in voivodeships:
        voivodship = voivodeships[key]
        last_page = get_max_pages(voivodship)
        print('downloading data for ', key)
        print('last page is ', last_page)
        for i in range(1, last_page):
            download_start = datetime.now()
            print(f'Im on page number {i} of {last_page}')
            try:
                cepik_link = f"https://api.cepik.gov.pl/pojazdy?wojewodztwo={voivodship}&data-od=20200601&data-do=20201201&typ-daty=1" \
                             f"&tylko-zarejestrowane=true&pokaz-wszystkie-pola=true&limit=500&page={i}"
                response = requests.get(cepik_link, verify=False)
                response_json = response.json()
                response_json_data = response_json['data']
                df.append(pd.json_normalize(response_json_data))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                pass

    return df

# suma = 0
# v = get_voivodeship_dictionary()
# for key in v:
#     suma += get_max_pages(v[key])
#     print(f'{key} got pages: {get_max_pages(v[key])}')
#
# print(suma)

# voivodeships_dictionary = get_voivodeship_dictionary()
# data = get_cars_dataframe(voivodeships_dictionary)
