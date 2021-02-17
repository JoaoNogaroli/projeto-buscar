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
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
    driver.get(url)
    texto = driver.find_element_by_xpath('//*[@id="custom_html-87"]/div/ul/li[1]/a')
    texto_alt = texto.get_attribute('innerHTML')
    return texto_alt


@app.route('/')
def index():
    a = teste()
    return render_template('index.html', casa = "TESS")


if __name__== "__main__":
    app.run(debug=True, port=port)
