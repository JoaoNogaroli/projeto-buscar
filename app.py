from celery import Celery
from celeryconfig import CELERY_BROKER_BACKEND,result_backend
from flask import Flask, render_template, url_for, request, session, redirect, jsonify
import json
import os
from script import teste
from task import debug_task
import time
import pyrebase
from firebase import firebase
import sys

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))
      
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


@app.route('/')
def index():    
    
    return render_template('index.html')

@app.route('/segundapag/')
def segundapagina():    
    
    return render_template('segundapag.html')

   
    
def salvar_id(user_uid,task_id,txt_pesquisa):
    database.child("Pesquisa/"+user_uid).set({
                "Txt_pesquisado":  txt_pesquisa,
                "Task_id" : task_id
    })


@app.route('/segundapag/', methods = ['POST'])
def pegar():
    word = request.form['jojo']
    user = request.form['user_email']   
    user_uid = request.form['user_uid']
    a = debug_task.delay(word)
    task_id = a.id
    time.sleep(1)
    salvar_id(user_uid,task_id, word)
    while a.status == "PENDING": 
        
        return render_template('wait.html',a_value =user, a_id=task_id)
        break
    a_value = (a.get())[0]
    b_value = (a.get())[1]
    
    return render_template('teste.html', a = a_value, b= b_value)
#


if __name__== "__main__":
    app.run(debug=True, port=port)
