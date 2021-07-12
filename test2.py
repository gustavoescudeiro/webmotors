from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
from unidecode import unidecode

df = pd.read_csv('webmotors.csv', sep = ';', decimal = ',')
links = df['link']

list_df = []
for i in links:
    driver = webdriver.Chrome()
    driver.get(i)
    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        anomodelo = soup.find(id=['VehiclePrincipalInformationYear']).get_text()
        quilometragem = soup.find(id=['VehiclePrincipalInformatiOnodometer']).get_text()
        carroceria = soup.find(id=['VehiclePrincipalInformationBodyType']).get_text()
        combustivel = soup.find(id=['VehiclePrincipalInformationFuel']).get_text()
        cor = soup.find(id=['VehiclePrincipalInformationColor']).get_text()
        aceita_troca = soup.find(id=['VehicleCharacteristicPos1']).get_text()
        todas_revisoes_concessionaria = soup.find(id=['VehicleCharacteristicPos2']).get_text()
        todas_revisoes_concessionaria = soup.find(id=['VehicleCharacteristicPos2']).get_text()
        containers = soup.find_all('div', class_=['VehicleDetails__container'])

        for container in containers:
            infos = soup.find_all('li', class_=['VehicleDetails__list__item'])

        list_title = []
        list_value = []
        list_more_values = []
        for info in infos:
            titles = soup.find_all('h2', class_=['VehicleDetails__list__item__title'])
            values = soup.find_all('strong', class_=['VehicleDetails__list__item__value'])
        for title in titles:
            list_title.append(title.get_text())
        for value in values:
            list_value.append(value.get_text())

        more_values = soup.find_all('h3', class_=['VehicleDetails__list__item__value'])
        for value_ad in more_values:
            list_more_values.append(value_ad.get_text())

        comentario = soup.find(id=['VehicleAboutInformationDescription']).get_text()
        driver.quit()
        data = {'column': list_title, 'value': list_value}
        dataframe = pd.DataFrame(data)
        dataframe.set_index(['column'], inplace = True)
        dataframe = dataframe.T.reset_index(drop = False)
        dataframe.drop(['index'], axis = 1, inplace = True)
        dataframe['link'] = i

    except:
        print('nope')


    list_df.append(dataframe)


t = pd.concat(list_df, axis = 0).reset_index(drop = True)
colunas = t.columns.str.lower().str.replace(" ", "_").to_list()

novas_colunas = []
for i in colunas:
    novas_colunas.append(unidecode(i))

novas_colunas = ["nao_identificado" if x == '' else x for x in novas_colunas]

t.columns = novas_colunas

t.to_csv('all_cars.csv', sep = ';', decimal = ',', encoding = 'utf-8', index = False)



print('a')