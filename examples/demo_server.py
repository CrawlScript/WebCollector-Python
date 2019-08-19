# coding=utf-8
from flask import Flask
import time
import random
app = Flask(__name__)

@app.route("/")
def index():
    time.sleep(2)
    return "ok"

app.run()
