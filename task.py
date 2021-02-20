import os
from celery import Celery
from celeryconfig import CELERY_BROKER_BACKEND,result_backend
from flask import Flask, render_template, url_for, request, session
import json
import pika
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import cgi
import os
import sqlalchemy
import time
import re
import firebase

celery = Celery('task',broker=CELERY_BROKER_BACKEND, backend=result_backend)

#celery.config_from_object('celeryconfig')
firebaseConfig = {
    "apiKey": "AIzaSyD-5dd-c9GUcNnJbzZwJsGyj5Mi077EJv0",
    "authDomain": "celery-db.firebaseapp.com",
    "databaseURL": "https://celery-db-default-rtdb.firebaseio.com",
    "projectId": "celery-db",
    "storageBucket": "celery-db.appspot.com",
    "messagingSenderId": "263395259912",
    "appId": "1:263395259912:web:a45cc33a1140500971c3bd",
    "measurementId": "G-6JT7B5X9DY"
  };
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();

database = firebase.database()


@celery.task
def debug_task(word):
    url = "https://riovagas.com.br/"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('window-size=1400,900')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    #------>Usar no deploy
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
    #Usar nos testes,
    #driver = webdriver.Chrome(executable_path=r"C:\\Users\\joaon\\Desktop\\selenium-webdriver\\chromedriver", chrome_options=chrome_options)
    driver.get(url)

    btn_input = driver.find_element_by_class_name("searchform__group-input")
    btn_input.send_keys(word)
    btn_input.send_keys(Keys.ENTER)
    
   
    results_sem_formato = []
    results_com_formato = []

    links_resultados = []

    resultado_final = []
    rl = []
    lr = []



    element = driver.find_elements_by_xpath("//div[@class='vce-loop-wrap custom-lay-b']//h2//a")

    for i in range(0, 5):
        try:
            html_content = element[i].get_attribute('innerHTML')
            html_todo = element[i].get_attribute('href')
            #print("Nome: ", html_content)
            html_formatado = html_content.split('R$')
            #print(i," Nome Formatado :", html_formatado[0])
            #print(i, html_todo)
            results_sem_formato.append(html_content)
            results_com_formato.append(html_formatado[0].lower())
            links_resultados.append(html_todo)
            i = i + 1
        except Exception:
            #print("Error Exception: ", {i})
            continue

    #print("TESTE 1: ", results_sem_formato)    
    #print("TESTE 2: ", links_resultados)    
    #, links_resultados[0]
    print("MOMENTO 1--------- SE PASSEI DAQUI, RETIRA TUDO ATRAS")
    #---------->
    a = word.split()
    print("TESTANDO: ", a)
    print("RESULTADOS: ", results_com_formato)
    for i in range(0, 5):
            if a[0] and a[1] in results_com_formato[i]:
                #print("Nome formatado: ",results_com_formato[i])
                #print("--------------------//-----------------")
                #print("Nome Completo: ", results_sem_formato[i])
                rl.append(results_sem_formato[i])
               # print(f"item {i} contem o texto")
               # print(i, " link para a vaga: ", links_resultados[i])
                lr.append(links_resultados[i])
            # resultado_final.extend(results_sem_formato[i], links_resultados[i])
                #resultado_final.append(links_resultados[i])
                listar_resultados = list((rl, lr))
                resultado_final.append(listar_resultados)
                #print("--------------------//-----------------")
        
            else:
                print("Error  ao content MOMENTO 1")
    print("Resultado antes do momento 2: ", resultado_final)
    print("MOMENTO 2 ---- SE PASSOU DAQUI< RETIRA TUDO ANTES")   
    # AQUI EU JA PEGUEI VALORES DA 1º pÁGINA, e VOU COMEÇAR O A LISTAR RESULTADO DE TODAS AS PÁGINAS    
    listar_paginas = []
    time.sleep(2.5)

    for i in range (0, 15):
        time.sleep(0.5)
        try:
            page_numbers = []
            page_numbers = driver.find_elements_by_xpath("//a[@class='page-numbers']")
            print("Numero da página: ", page_numbers[i].get_attribute('innerHTML'))
            listar_paginas.append(page_numbers[i].get_attribute('innerHTML'))
        except Exception:
            print(f"----Não há pagina nº: {i}")

    print(listar_paginas)
    print("Teste ultimo numero de pagina: ", listar_paginas[-1])
    lastpag = int(listar_paginas[-1])
    #.get_attribute('innerHTML')
    print("--------------       INICIANDO => MUDANÇA DE PAGINA")
    time.sleep(2.5)

    for i in range(0, lastpag-1):
        time.sleep(2.5)
        try:
            elemento_tres = driver.find_element_by_xpath("//a[@class='next page-numbers']")
            driver.execute_script("arguments[0].click();", elemento_tres)
            print(i, "Trocando de pagina")

            ##---- TESTANDO A FUNÇÂO DE BUSCAR ITEM
            results_sem_formato = []
            results_com_formato = []

            links_resultados = []

            element = driver.find_elements_by_xpath("//div[@class='vce-loop-wrap custom-lay-b']//h2//a")
            element_dois = driver.find_elements_by_xpath("//div[@class='vce-loop-wrap custom-lay-b']//h2//a")

            for i in range(0, 5):
                try:
                    html_content = element[i].get_attribute('innerHTML')
                    html_todo = element_dois[i].get_attribute('href')
                    # print("Nome: ", html_content)
                    html_formatado = html_content.split('R$')
                    # print(i," Nome Formatado :", html_formatado[0])
                    print(i, html_todo)
                    results_sem_formato.append(html_content)
                    results_com_formato.append(html_formatado[0].lower())
                    links_resultados.append(html_todo)


                    i = i + 1
                except Exception:
                    print("Error Exception: ", {i})
                    continue
            a = word.split()
            print("TESTANDO: ", a)
            print("RESULTADOS: ", results_com_formato)
            for i in range(0, 5):
                if a[0] and a[1] in results_com_formato[i]:
                    # print("Nome formatado: ",results_com_formato[i])
                    print("--------------------//-----------------")
                    print("Nome Completo: ", results_sem_formato[i])

                    print(f"item {i} contem o texto")
                    print(i, " link para a vaga: ", links_resultados[i])
                    rl.append(results_sem_formato[i])
                    lr.append(links_resultados[i])
                    print("--------------------//-----------------")
                else:
                    print("Error  ao content")

            i = i+1
            time.sleep(2)
        except Exception as e:
            print(f"Errro na troca de págica {i}")
            continue
    #print("MOMENTO FINAL ----- VTESTE")
    #driver.quit()

    #print("/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------")
    #print(resultado_final)
    #print("/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------")
       
    #print("/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------")
     

    #print("info:     /////////////---------/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------")
    info=dict(zip(rl,lr))
    print(info)
   # print(" lissst :     /////////////---l  ------/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------")
    #print(list(info.values()))
    #print("/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------")
    #print("LISTA 1: ", rl)
    #print("/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------/////////////---------")

    #print("LISTA 2: ", lr)

    driver.close()

    for i in range (0,15):
        try:
            database.child("TESTE").child(f'Resultado{i}').set({
                f'NomeDaVaga{i}': rl[i],
                f'LinkDaVaga{i}': lr[i]
                })
        except Exception:
            print("error no teste")
            continue
    



    print("ACABOu")
    return rl, lr
    