from flask import Flask, render_template, url_for, request, session
import json
import os
import json



app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))


def teste():
    a =1
    return a


@app.route('/')
def index():
    a = teste()
    return render_template('index.html', casa=a + "TESTE")


if __name__== "__main__":
    app.run(debug=True, port=port)
