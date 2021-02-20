from celery import Celery
from celeryconfig import CELERY_BROKER_BACKEND,result_backend
from flask import Flask, render_template, url_for, request, session, redirect, HttpResponse
import json
import os
from script import teste
from task import debug_task

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))
      

@app.route('/', methods = ['POST'])
def pegar():
    word = request.form['jojo']
    
    a = debug_task.delay(word)
    while a.status == "PENDING": 
        return HttpResponse('wait')
    a_value = (a.get())[0]
    b_value = (a.get())[1]

    
    return render_template('teste.html', a = a_value, b= b_value)


@app.route('/')
def index():    
    
    return render_template('index.html')


if __name__== "__main__":
    app.run(debug=True, port=port)
