from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import numpy as np


class item(object):  # cria objetivo (imóvel) que terá suas características adicionadas a uma lista
    lista_de_item = []

    def __init__(self, link, preco, modelo, anomodelo, cidade):
        self.link = link
        self.preco = preco
        self.modelo = modelo
        self.anomodelo = anomodelo
        # self.quilometragem = quilometragem
        self.dic = {'link': link, 'preco': preco, 'modelo': modelo, 'anomodelo': anomodelo, 'cidade': cidade}
        item.lista_de_item.append(self.dic)  # adiciona cada imóvel em um dicionário o coloca numa lista


def button_click(driver):
    try:
        btn = driver.find_element_by_xpath('//*[@id="ButtonCarriesMoreCars"]')
        btn.click()
        roll_page(driver)

    except:
        time.sleep(3)
        captura(driver)
    # roll_page(driver)


def find_button_and_press(driver):
    # btn = driver.find_element_by_class_name('Button Button--more-items')
    btn = driver.find_element_by_xpath('//*[@id="ButtonCarriesMoreCars"]')

    print(btn)
    btn.click()
    roll_page(driver)


# if btn != None:
# print(btn)
# else: roll_page(driver)


def roll_page(driver):
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

    match = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        print(lenOfPage, lastCount)
        if lastCount == lenOfPage:
            match = True
    button_click(driver)

    print('finalizado')


def busca(url):
    lista_ips = ['200.147.153.131:80',
                 '200.245.9.140:8080',
                 '191.232.170.36:80',
                 '187.87.38.28:53281',
                 '177.99.206.82:8080',
                 '187.87.38.28:53281',
                 '186.225.110.166:8080',
                 '191.232.170.36:80'
                 ]

    random = np.random.randint(0, len(lista_ips))
    PROXY = lista_ips[random]

    # setando proxy para evitar que site nos bloqueie:
    # webdriver.DesiredCapabilities.CHROME['proxy']={
    # "httpProxy":PROXY,
    # "ftpProxy":PROXY,
    # "sslProxy":PROXY,
    # "proxyType":"MANUAL",
    # }

    driver = webdriver.Chrome()
    # driver.minimize_window()
    driver.get(url)
    # html = driver.page_source
    # soup = BeautifulSoup(html, 'html.parser')
    time.sleep(60)
    # xpath = '//*[@id="proximaPagina"]'
    # btn = driver.find_element_by_xpath(xpath)
    # btn.click()
    # carros = soup.find_all('a')
    # tudo = soup.find('div', class_= ['ContainerCardVehicle'])
    # print(tudo)

    roll_page(driver)
    captura(driver)


def captura(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(10)

    print('capturando')

    # time.sleep(10)

    carros = soup.find_all('div', class_=['sc-kvZOFW ecltnr'])

    #	print(carros)
    for carro in carros:

        print(carro)
        preco = carro.find('strong', class_=['sc-eHgmQL hTaWtZ']).get_text()
        print(preco)

        modelo = carro.find('h3', class_=['sc-jDwBTQ czFfrF']).get_text()
        print(modelo)

        anomodelo = carro.find('span', class_=['sc-brqgnP UuoTk']).get_text()
        print(anomodelo)

        cidade = carro.find('span', class_=['sc-hSdWYo gQLPlL']).get_text()
        print(cidade)

        # quilometragem = carro.find_all('div', class_=['sc-kkGfuU ddBzEJ'])
        # quilometragem = str(quilometragem)
        # quilometragem = quilometragem[60:69]
        # print(quilometragem)

        link = carro.find('a')['href']
        print(link)

        item(link, preco, modelo, anomodelo, cidade)

        with open('C:\\Users\\Pichau\\Documents\\projetos_py\\webmotorsf.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, item.lista_de_item[0].keys())
            writer.writeheader()
            for d in item.lista_de_item:
                writer.writerow(d)



busca('https://www.webmotors.com.br/carros/sp-sao-paulo/hyundai/hb20?estadocidade=S%C3%A3o%20Paulo%20-%20S%C3%A3o%20Paulo&marca1=HYUNDAI&modelo1=HB20&idcmpint=t1:c17:m07:webmotors:modelo::hyundai%20hb20&autocomplete=hb2')