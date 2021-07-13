from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from unidecode import unidecode
import numpy as np



def get_car_info(url_car_list = []):

    list_df = []
    links = url_car_list
    for i in links:
        driver = webdriver.Chrome()
        driver.get(i)
        time.sleep(1)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            anomodelo = soup.find(id=['VehiclePrincipalInformationYear']).get_text()
        except:
            anomodelo = np.nan

        try:
            quilometragem = soup.find(id=['VehiclePrincipalInformatiOnodometer']).get_text()
        except:
            quilometragem = np.nan

        try:
            carroceria = soup.find(id=['VehiclePrincipalInformationBodyType']).get_text()
        except:
            carroceria = np.nan

        try:
            combustivel = soup.find(id=['VehiclePrincipalInformationFuel']).get_text()
        except:
            combustivel = np.nan

        try:
            cor = soup.find(id=['VehiclePrincipalInformationColor']).get_text()
        except:
            cor = np.nan

        try:
            aceita_troca = soup.find(id=['VehicleCharacteristicPos1']).get_text()
        except:
            aceita_troca = np.nan

        try:
            todas_revisoes_concessionaria = soup.find(id=['VehicleCharacteristicPos2']).get_text()
        except:
            todas_revisoes_concessionaria = np.nan


        # getting aditional info
        containers = soup.find_all('div', class_=['VehicleDetails__container'])

        for container in containers:
            infos = soup.find_all('li', class_=['VehicleDetails__list__item'])

        list_title = []
        list_value = []
        list_more_values = []
        for info in infos:
            try:
                titles = soup.find_all('h2', class_=['VehicleDetails__list__item__title'])
            except:
                titles = np.nan
            try:
                values = soup.find_all('strong', class_=['VehicleDetails__list__item__value'])
            except:
                values = np.nan

        for title in titles:
            try:
                list_title.append(title.get_text())
            except:
                list_title.append(np.nan)

        for value in values:
            try:
                list_value.append(value.get_text())
            except:
                list_value.append(np.nan)

        more_values = soup.find_all('h3', class_=['VehicleDetails__list__item__value'])
        for value_ad in more_values:
            try:
                list_more_values.append(value_ad.get_text())
            except:
                list_more_values.append(np.nan)
        try:
            comentario = soup.find(id=['VehicleAboutInformationDescription']).get_text()
        except:
            comentario = np.nan

        driver.quit()
        data = {'column': list_title, 'value': list_value}
        dataframe = pd.DataFrame(data)
        dataframe.set_index(['column'], inplace = True)
        dataframe = dataframe.T.reset_index(drop = False)
        dataframe.drop(['index'], axis = 1, inplace = True)
        dataframe['link'] = i




        list_df.append(dataframe)


    t = pd.concat(list_df, axis = 0).reset_index(drop = True)
    colunas = t.columns.str.lower().str.replace(" ", "_").to_list()

    novas_colunas = []
    for i in colunas:
        novas_colunas.append(unidecode(i))

    novas_colunas = ["nao_identificado" if x == '' else x for x in novas_colunas]

    t.columns = novas_colunas

    t.to_csv('more_info.csv', sep = ';', decimal = ',', encoding = 'utf-8', index = False)

