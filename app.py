from flask import Flask
import os
app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))


@app.route('/')
def index():
    return "<h1>olá</h1>"


@app.route('/sobre')
def sobre():
    return "<h1>sobre</h1>"

if __name__== "__main__":
    app.run(debug=True, port=port)
