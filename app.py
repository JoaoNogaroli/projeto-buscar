from flask import Flask, render_template, url_for, request, session
import json
import os
import json
from flask_executor import Executor
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

executor = Executor(app)

def teste():
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
    btn_input.send_keys("estágio informática")
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
    print("TESTE 2: ", links_resultados)    

    return results_sem_formato[0], links_resultados[0]


@app.route('/')
def index():
    a, b = teste()

    return render_template('index.html', a = a, b =b)


if __name__== "__main__":
    app.run(debug=True, port=port)
