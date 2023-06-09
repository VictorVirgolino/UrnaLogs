# import pandas as pd
from time import sleep
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
# import sqlalchemy
# import subprocess
# import time
# import numpy as np
import os 
import shutil
"""
Objetivo: Realizar Web Scrapping para recuperar os dados do 1º e 2º turnos das eleições ocorridas,
respectivamente, nos dias 02/10/2022 e 30/10/2022, e realizar uma análise exploratória dos dados.
"""

turno = 'https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e544/dados-de-urna/boletim-de-urna' #1 Turno
# turno = 'https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e545/dados-de-urna/boletim-de-urna'#2 Turno

absolute_path =  os.path.dirname(__file__)
path = os.path.join(absolute_path, "WorkStation\\temp")
path_to = os.path.join(absolute_path, "WorkStation\\")

path_download = path.replace('/', '\\').replace('\'', '\\')
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : path_download}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("start-maximized")
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')

if(not os.path.exists(path_to)):
    os.mkdir(path_to)
os.chdir(path_to)

start_estado = 5;#13
start_municipio = 1;#39
start_zona = 2;#3
start_secao = 2;

cont = True;
last= ''
flag = True
limite_downloads = 400
contador = 1
error = False

#dataframe dos municipios
colunas_zonas = ["Zona", "Município", "Estado"]
zonas = pd.DataFrame(columns=colunas_zonas)

# if(os.path.exists(path_to)):
#             shutil.rmtree(path_to)
#             os.mkdir(path_to)
#             error = False

while(True):

    try:

        a=0

        if(os.path.exists(path)):
            shutil.rmtree(path)
            error = False
       
        nav = webdriver.Chrome(options=chrome_options)

        nav.get(turno)

        print("Clicar em Alterar Localidade")
        sleep(1)
        nav.find_element(By.XPATH, "//div[@title='Alterar localidade']").click();
        sleep(1)
        WebDriverWait(nav, 60).until(
            EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='uf']"))
            
        )
        # Selecionar estado
        nav.find_element(By.XPATH, "//input[@formcontrolname='uf']").click()
        WebDriverWait(nav, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='listbox']//mat-option"))
        )
        num_estados = nav.find_elements(By.XPATH, "//div[@role='listbox']//mat-option")
        
        print("Total de Estados: " + str(len(num_estados)))
        #if Continue Set Estado Inicial:
        if(cont):
            num = start_estado
        else:
            num = 1

        #Seleciona o Estado
        for estado in range(num, len(num_estados)+1):
            
            nome_estado = nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[%d]//span"%(estado)).text
            
            if(not os.path.exists(nome_estado)):
                os.mkdir(nome_estado)
            print("||------------ Estado  "+ str(nome_estado)  + " ------------||")
            sleep(1)
            nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[%d]"%(estado)).click()
            num_municipios = nav.find_elements(By.XPATH, "//div[@role='listbox']//mat-option")
            print("Total de Municipios: " + str(len(num_municipios)))
            path_estado = path_to + nome_estado
            #if Continue Set Municipio Inicial:
            if(cont):
                num = start_municipio
            else:
                num = 1
            #Seleciona o municipio
            for municipio in range(num, len(num_municipios)+1):
                nome_municipio = nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[%d]//span"%(municipio)).text
                if(not os.path.exists(nome_municipio)):
                    os.mkdir(nome_municipio)
                print("|----------   "+ str(nome_municipio)  + " ----------|")
                sleep(1)
                nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[%d]"%(municipio)).click()
                nav.find_element(By.XPATH, "//ion-footer//div//ion-button").click()
                WebDriverWait(nav, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//mat-form-field[1]"))
                )
                #Selecionando a Zona
                nav.find_element(By.XPATH, "//mat-form-field[1]").click()
                num_zonas= nav.find_elements(By.XPATH, "//div[@role='listbox']//mat-option")
                print("Total de Zonas: " + str(len(num_zonas)-1))
                path_municipio = path_to+nome_municipio
                #if Continue Set Zona Inicial:
                if(cont):
                    num = start_zona
                else:
                    num = 2
                #Seleciona a Zona
                for zona in range(num, len(num_zonas)+1):
                    sleep(1)
                    nome_zona = nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[%d]//span"%(zona)).text
                    
                    #adicionar zona ao dataframe
                    nova_zona = pd.DataFrame([[nome_zona, nome_municipio, nome_estado]], columns=colunas_zonas)
                    zonas = pd.concat([zonas, nova_zona], ignore_index=True)

                    if(not os.path.exists(nome_zona)):
                        os.mkdir(nome_zona)
                    print("--------|   "+ str(nome_zona)  + " |--------")
                    sleep(1)
                    nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[%d]"%(zona)).click()
                    nav.find_element(By.XPATH, "//mat-form-field[2]").click()
                    num_secoes= nav.find_elements(By.XPATH, "//div[@role='listbox']//mat-option")
                    print("Total de Seções: " + str(len(num_secoes)-1))
                    path_zona = path_to+nome_zona
                    #if Continue Set Seção Inicial:
                    if(cont):
                        num = start_secao
                        cont = False 
                    else:
                        num = 2
                        cont = False
                    #Seleciona a Seção
                    
                    for secao in range(num,len(num_secoes)+1):
                        
                        # exist = os.path.isdir(path) 
                        # while(exist):
                        #     print("temp não enviado...")
                        #     sleep(5)
                        #     if(a==3):
                        #         dest = path_to+"\\"+nome_zona+"\\"+last
                        #         print(dest)
                        #         if(os.path.exists(dest)):
                        #             shutil.rmtree(dest)
                        #         shutil.move(path,dest)
                        #         a = 0
                        #     exist = os.path.isdir(path) and any(fname.endswith('.zip') for fname in os.listdir(dest))                    
                        #     a+=1
                        

                        os.mkdir('temp')
                        sleep(1)
                        nome_secao = nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[%d]//span"%(secao)).text
                        
                        print("/------   "+ str(nome_secao)  + " ------\\")
                        
                        nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[%d]"%(secao)).click()
                        nav.find_element(By.XPATH, "//button").click()
                        WebDriverWait(nav, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//li[@class='mr-5 li-active-2 ng-star-inserted']//a"))
                        )
                        nav.find_element(By.XPATH, "//li[@class='mr-5 li-active-2 ng-star-inserted']//a").click()
                        nav.find_element(By.XPATH, "//mat-form-field[2]").click()
                        dest = path_to+"\\"+nome_zona+"\\"+nome_secao
                        last = nome_secao
                        sleep(2)

                        #checar se a pasta temp existe e se o arquivo zip está nela
                        if(os.path.isdir(path) and any(fname.endswith('.zip') for fname in os.listdir(path))):
                            shutil.move(path,dest)

                            while(os.path.isdir(path) or not(os.path.isdir(dest) and any(fname.endswith('.zip') for fname in os.listdir(dest)))):
                                if(a == 5):
                                    print('last: ', last)
                                    raise Exception('Arquivo não foi movido corretamente! Reiniciando....')
                                sleep(2)
                                print('Arquivo ainda não foi movido... ', a)
                                a += 1
                            
                            


                            
    
                        
                        else:
                            print('last: ', last)
                            raise Exception('Arquivo zip não foi baixado! Reiniciando....')

                        a = 0
                        sleep(1)
                        


                        # checar se a pasta foi movida e se o arquivo se encontra dentro dela
                        # if(not any(fname.endswith('.zip') for fname in os.listdir(path))):
                        #     print('last: ', last)
                        #     raise Exception('Limite de downloads alcançado! Reiniciando....')

                        # sleep(1)
                    
                        print(path_to+"\\"+nome_zona+"\\"+nome_secao + ' enviado com sucesso')

                        if(contador >= limite_downloads):
                            print('last: ', last)
                            raise Exception('Limite de downloads alcançado! Reiniciando....')
                        
                        contador += 1

                        
                        
                        
                    print("Fim das Seções")
                    shutil.move(path_zona,path_municipio)
                    nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[2]").click()
                    nav.find_element(By.XPATH, "//mat-form-field[1]").click()
                print("Fim das Zonas")
                shutil.move(path_municipio,path_estado)
                nav.find_element(By.XPATH, "//div[@role='listbox']//mat-option[2]").click()
                nav.find_element(By.XPATH, "//div[@title='Alterar localidade']").click();
            
                
                sleep(1)
            # Selecionar estado
            print("Fim do Municipios")
            # print("Describe:", zonas.describe())
            # zonas.to_csv(path_to + '/zonas.csv')
            # sleep(1)
            nav.find_element(By.XPATH, "//input[@formcontrolname='uf']").click()
            

    except Exception as e:
        print(e)
        contador = 0
        cont = True
        start_estado = estado
        start_municipio = municipio
        start_zona = zona
        last = nome_secao
        dest = path_to+"\\"+nome_zona+"\\"+last
        start_secao = secao

        if(os.path.exists(dest)):
            shutil.rmtree(dest)

        nav.close()
        nav.quit()


    # finally:
    #     print("ok")
    #     nav.close()
    #     nav.quit()


