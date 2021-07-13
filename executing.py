from get_page_info import *
from get_specific_car_info import *

#get_all_cars('https://www.webmotors.com.br/carros/sp-santo-andre/hyundai/hb20?estadocidade=S%C3%A3o%20Paulo%20-%20Santo%20Andr%C3%A9&tipoveiculo=carros&localizacao=-23.6380539,-46.5341478x0km&marca1=HYUNDAI&modelo1=HB20')

df_basic = pd.read_csv('basic_info.csv', sep = ';', decimal = ',')
links = df_basic['link']

get_car_info(links)
