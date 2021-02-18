from flask import Flask, render_template, url_for, request, session
import json
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import cgi
import os



def teste(word):
    
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
            print(i, html_todo)
            results_sem_formato.append(html_content)
            results_com_formato.append(html_formatado[0].lower())
            links_resultados.append(html_todo)
            i = i + 1
        except Exception:
            print("Error Exception: ", {i})
            continue

    print("TESTE 1: ", results_sem_formato)    
    #print("TESTE 2: ", links_resultados)    
    #, links_resultados[0]
    driver.close()

    #---------->
    a = word.split()
    print("TESTANDO: ", a)
    print("RESULTADOS: ", results_com_formato)
    for i in range(0, 5):
        if a[0] and a[1] in results_com_formato[i]:
            #print("Nome formatado: ",results_com_formato[i])
            print("--------------------//-----------------")
            print("Nome Completo: ", results_sem_formato[i])
            rl.append(results_sem_formato[i])
            print(f"item {i} contem o texto")
            print(i, " link para a vaga: ", links_resultados[i])
            lr.append(links_resultados[i])
        # resultado_final.extend(results_sem_formato[i], links_resultados[i])
            #resultado_final.append(links_resultados[i])
            listar_resultados = list((rl, lr))
            resultado_final.append(listar_resultados)
            print("--------------------//-----------------")
        else:
            print("Error  ao content")



    return rl, lr