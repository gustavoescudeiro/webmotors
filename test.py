from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import numpy as np


url = 'https://www.webmotors.com.br/carros/sp-sao-paulo/hyundai/hb20?estadocidade=S%C3%A3o%20Paulo%20-%20S%C3%A3o%20Paulo&marca1=HYUNDAI&modelo1=HB20&idcmpint=t1:c17:m07:webmotors:modelo::hyundai%20hb20&autocomplete=hb2'

driver = webdriver.Chrome()
driver.get(url)
time.sleep(10)

lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

match = False
while (match == False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    print(lenOfPage, lastCount)
    if lastCount == lenOfPage:
        match = True


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
time.sleep(10)
print('capturando')
carros = soup.find_all('div', class_=['sc-cmthru jSUxTP'])

for carro in carros:
    print(carro)
    preco = carro.find('strong', class_=['sc-kvZOFW knsOia']).get_text()
    print(preco)

    modelo = carro.find('h3', class_=['sc-bbmXgH fEaLmM']).get_text()
    print(modelo)

    anomodelo = carro.find('span', class_=['sc-dNLxif xTPZF']).get_text()
    print(anomodelo)

    cidade = carro.find('span', class_=['sc-frDJqD cXlpPT']).get_text()
    print(cidade)


print('fim')