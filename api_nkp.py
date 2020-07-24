import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from proxy.const import API_BOT_NAME, API_BOT_PASS, URL

# API classic
def api_c():
    data1 = requests.get('...')
    print(data1.content)
    soup1 = BeautifulSoup(data1.text, 'html.parser')
    print(soup1)
    return soup1


#API flask
def api_f():
    data = requests.get('...')
    soup = BeautifulSoup(data.text, 'html.parser')
    print(soup)
    return f'{soup}'

# Авторизация
def api_f_auth():
    data = requests.get(URL+API_BOT_NAME+API_BOT_PASS)
    soup = BeautifulSoup(data.text, 'html.parser')
    print(soup)
    return f'{soup}'
