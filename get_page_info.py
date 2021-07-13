from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_all_cars(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    button = soup.find('div', class_=['sc-bdVaJa bjRMar'])
    print(button)
    if not button is None:
        btn = driver.find_element_by_css_selector('#root > div.sc-bdVaJa.bjRMar > div.sc-htpNat.iPWKQm > button')
        btn.click()


    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

    match = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        button = soup.find('div', class_=['ContainerButtons__details__buttons'])
        print(button)
        if not button is None:
            btn = driver.find_element_by_css_selector('#ButtonCarriesMoreCars')
            btn.click()


        print(lenOfPage, lastCount)
        if lastCount == lenOfPage:
            match = True


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(10)
    print('capturando')
    #carros = soup.find_all('div', class_=['ContainerCardVehicle ads_align'])
    precos = soup.find_all('strong', class_=['sc-kvZOFW knsOia'])
    links = soup.find_all('div', class_=['sc-hMFtBS cVTeoI'])
    precos_sugeridos = soup.find_all('div', class_=['sc-hMFtBS cVTeoI'])
    modelos = soup.find_all('h3', class_=['sc-bbmXgH fEaLmM'])
    anomodelos = soup.find_all('span', class_=['sc-dNLxif xTPZF'])
    cidades = soup.find_all('span', class_=['sc-frDJqD cXlpPT'])


    list_precos = []
    for i in precos:
        list_precos.append(float(i.get_text().replace("R$", "")))
        print(i.get_text())

    list_links = []
    for i in links:
        list_links.append(i.find('a', target=['_blank'])['href'])
        print(i)

    verify_zerokm_publicidade = []
    for i in precos_sugeridos:
        verify_zerokm_publicidade.append(i.get_text())
        print(i.get_text())

    matching = []
    for i in verify_zerokm_publicidade:
        if 'preço sugerido' in i:
            retorno = 0
        else:
            retorno = 1
        matching.append(retorno)


    list_modelos = []
    for i in modelos:
        list_modelos.append(i.get_text())

    count = 0
    list_anomodelos = []
    list_km = []
    for i in anomodelos:
        if count % 2 == 0:
            list_anomodelos.append(i.get_text())
        else:
            list_km.append(i.get_text())
        count += 1

    data = {'link': list_links, 'preco': list_precos, 'valid_preco': matching}

    df = pd.DataFrame(data)
    df = df[df['valid_preco'] == 1]
    df.reset_index(drop = True, inplace = True)

    df['modelo'] = list_modelos
    df['anomodelo'] = list_anomodelos
    df['quilometragem'] = list_km

    df.to_csv('basic_info.csv', sep = ';', decimal = ',', index = False)
