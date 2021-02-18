from flask import Flask, render_template, url_for, request, session
import json
import os
from script import teste

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))
      

@app.route('/', methods = ['POST'])
def pegar():
    word = request.form['jojo']
    value_a, value_b = teste(word)
    return render_template('teste.html', value_a = value_a, value_b = value_b) 


@app.route('/')
def index():    
    
    return render_template('index.html')


if __name__== "__main__":
    app.run(debug=True, port=port)
