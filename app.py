# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,jsonify,redirect
from flask_cors import *
import requests
import random
import os
import linecache


app = Flask(__name__)
CORS(app, supports_credentials=True)

def get_cave():
    txt = open(os.getcwd()+'/cave.txt','rb')
    data = txt.read().decode('utf-8')
    txt.close()
    n = data.count('\n')
    i = random.randint(1, (n+1))
    line=linecache.getline(os.getcwd()+'/cave.txt',i)
    return str(line)

print("\033[42m" + get_cave() + "\033[0m" + "           " + "Powerd By RDPStudio")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api')
def api():
  type = request.args.get("encode")
  if type=="js":
    return '(function cave(){var cave="' + get_cave() + '";var dom=document.querySelector(".cave");Array.isArray(dom)?dom[0].innerText=cave:dom.innerText=cave;})()'
  elif type=="json":
    return jsonify({"code": 200, "cave": get_cave()})
  else:
    return get_cave()

if (__name__ == "__main__"):
    app.run(host = '0.0.0.0', port = 31000)
