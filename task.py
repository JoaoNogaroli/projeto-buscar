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
import pyrebase
from firebase import firebase
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
#Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig);

database = firebase.database()


@celery.task(bind=True)
def debug_task(self, word,user_uid):
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
    time.sleep(0.5)

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
    time.sleep(0.5)

    for i in range(0, lastpag-1):
        time.sleep(0.5)
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
            time.sleep(0.5)
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
            print("salvando :", i)
            database.child("Users/"+user_uid+"/"+"Pesquisa/"+"Lista_resultados/"+f"Resultado_Pesq{i}").set({
                    'NomeDaVaga': rl[i],
                    'LinkDaVaga': lr[i]
            })
            
        except Exception:
            continue
            
    



    print("ACABOu")
    return rl, lr
    
@celery.task(bind=True)
def debug_catho(self,txt_catho):
    #text = input("Digite o nome do cargo: ")
    url = "https://catho.com.br/"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('window-size=1400,900')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    #------>Usar no deploy
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options) #
    #Usar nos testes,
    #driver = webdriver.Chrome(executable_path=r"C:\\Users\\joaon\\Desktop\\selenium-webdriver\\chromedriver", chrome_options=chrome_options)#
    driver.get(url)
    #--------------       INICIANDO => Clique no input para digitar ======
    btn_input = driver.find_element_by_xpath("/html/body/div[1]/div[1]/header/div/div/div[3]/div/nav/ul/li[4]/a")
    #time.sleep(2.5)
    btn_input.send_keys(Keys.ENTER)

    btn_email = driver.find_element_by_xpath("/html/body/div[2]/div/div/main/div/div/div/div/article/div/form/div[1]/div/input")
    btn_email.send_keys("jv.nogaroli@gmail.com")
    btn_password = driver.find_element_by_xpath("/html/body/div[2]/div/div/main/div/div/div/div/article/div/form/div[2]/div/input")
    btn_password.send_keys("Peidoo237!")

    btn_entrar = driver.find_element_by_xpath("/html/body/div[2]/div/div/main/div/div/div/div/article/div/form/button")
    btn_entrar.send_keys(Keys.ENTER)
    time.sleep(2.5)

    #text = input("Digite o nome do cargo: ")
    #text = "estágio direito"
    time.sleep(2.5)

    btn_text = driver.find_element_by_xpath("/html/body/header/div[3]/form/div[1]/fieldset/label/input")

    btn_text.send_keys(txt_catho)

    btn_buscar = driver.find_element_by_xpath("/html/body/header/div[3]/form/div[1]/fieldset/input")
    btn_buscar.send_keys(Keys.ENTER)
    time.sleep(3.5)

    cidade = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/section/div/form/div[2]/div[1]/div/div/input")
    texto_cidade = "Rio de Janeiro"
    cidade.send_keys(texto_cidade)
    time.sleep(0.5)
    cidade.send_keys(Keys.DOWN)
    time.sleep(0.5)
    cidade.send_keys((Keys.ENTER))
    #botao_final = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/section/div/form/button[2]")
    #botao_final.send_keys(Keys.ENTER)
    time.sleep(3)
    itens = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/main/div[3]/div/div/section/ul/li/article/header/div/div/h2/a")
    valor = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/main/div[3]/div/div/section/ul/li/article/header/div/div/div")


    lista_nome = []
    lista_valor = []
    lista_href = []

    for i in range(0,10):
        time.sleep(1)
        try:
            item_nome = itens[i].get_attribute('innerHTML')
            item_valor = valor[i].get_attribute('innerHTML')
            item_href = itens[i].get_attribute('href')
            lista_nome.append(item_nome)
            lista_valor.append(item_valor)
            lista_href.append(item_href)
            print(item_nome)
            print(item_valor)
            print(item_href)
        except Exception:
            print("ERROR")
            continue

    """info = {}
    info = dict(zip(lista_nome, zip(lista_valor,lista_href)))
    print(info)"""

    listar_paginas = []
    for i in range (0, 15):
        try:
            page_numbers = []
            page_numbers = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/main/div[3]/div/div/section/div/nav/a")
            print("Numero da página: ", page_numbers[i].get_attribute('innerHTML'))
            listar_paginas.append(page_numbers[i].get_attribute('innerHTML'))
        except Exception:
            print("----Acabou---")

    print(listar_paginas)

    new_items = [item for item in listar_paginas if item.isdigit()]

    print(new_items)
    print("ULTIMO ITEM: ", new_items[-1])
    last_pag = int(new_items[-1])

    if (last_pag>5):
        last_pag = 5
    for i in range(0, last_pag-1):
        time.sleep(2)
        try:
            elemento_tres = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[3]/div/div/section/div[3]/nav/a[2]")
            driver.execute_script("arguments[0].click();", elemento_tres)
            time.sleep(4)
            itens = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/main/div[3]/div/div/section/ul/li/article/header/div/div/h2/a")
            valor = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/main/div[3]/div/div/section/ul/li/article/header/div/div/div")


            for i in range(0, 10):
                time.sleep(1)
                try:
                    item_nome = itens[i].get_attribute('innerHTML')
                    item_valor = valor[i].get_attribute('innerHTML')
                    item_href = itens[i].get_attribute('href')
                    lista_nome.append(item_nome)
                    lista_valor.append(item_valor)
                    lista_href.append(item_href)
                    print(item_nome)
                    print(item_valor)
                    print(item_href)
                except Exception:
                    print("ERROR")
                    continue



        except Exception:
            print("ERROR NA MUDANÇA DE PAGNA")

    print(lista_nome)
    print(len(lista_nome))
    driver.quit()
