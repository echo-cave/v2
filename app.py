# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,jsonify,redirect,Blueprint
from flask_cors import *
from flask_limiter import Limiter, HEADERS  # https://github.com/alisaifee/flask-limiter
from flask_limiter.util import get_remote_address
import flask_profiler
import requests
import random
import os
import linecache

# Config Start
RATELIMIT_STORAGE_URL = "redis://127.0.0.1:6379"  # 将被限制不可以再正常访问的请求放入缓存

app = Flask(__name__)
CORS(app, supports_credentials=True)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[], # 全局配置,一般不要配置
    storage_uri=RATELIMIT_STORAGE_URL,
    headers_enabled=True  # X-RateLimit写入响应头。
)

app.config["flask_profiler"] = {
    "enabled": True,
    "storage": {
        "engine": "sqlite"
    },
    "basicAuth":{
        "enabled": False,
        "username": "admin",
        "password": "admin"
    },
    "ignore": []
}


print("Updateing Database")
url = 'https://echo-cave.github.io/cave/cave.txt'
# Config End
r = requests.get(url)
with open("cave.txt", "w", encoding="utf-8") as f:
  f.write(str(r.text).strip())

def get_cave():
    txt = open(os.getcwd()+'/cave.txt','rb')
    data = str(txt.read().decode('utf-8'))
    txt.close()
    n = data.count('\n')
    i = random.randint(1, (n+1))
    line=linecache.getline(os.getcwd()+'/cave.txt',i)
    return str(line).strip()

print("\033[45mEcho-Cave v2.0.3-dev\033[0m" + "  " + "\033[46mPowerd By RDPStudio\033[0m")
print("\n")
print("\033[46m" + get_cave() + "\033[0m")

@app.route('/')
@limiter.exempt
def index():
    return render_template("index.html")

@app.route('/api')
@limiter.limit("4/second")
def api():
  type = request.args.get("encode")
  if type=="js":
    return '(function cave(){var cave="' + get_cave() + '";var dom=document.querySelector(".cave");Array.isArray(dom)?dom[0].innerText=cave:dom.innerText=cave;})()'
  elif type=="json":
    return jsonify({"code": 200, "cave": get_cave()})
  else:
    return get_cave()

flask_profiler.init_app(app)

urlPath = "statics"

fp = Blueprint(
        'statics', __name__,
        url_prefix="/" + urlPath,
        static_folder="statics_template/", static_url_path='/static/dist')

@fp.route("/".format(urlPath))
def index():
    return fp.send_static_file("index.html")

app.register_blueprint(fp)

if (__name__ == "__main__"):
    app.run(host = '0.0.0.0', port = 31000, debug=False)
