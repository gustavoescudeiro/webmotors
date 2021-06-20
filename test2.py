from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time

df = pd.read_csv('webmotors.csv', sep = ';', decimal = ',')
links = df['link']



driver = webdriver.Chrome()
driver.get(links[0])
time.sleep(10)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

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





print('a')