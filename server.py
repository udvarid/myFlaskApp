from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('index.html')

@app.route("/index.html")
def my_index():
    return render_template('index.html')

@app.route("/gameOfLife.html")
def twocolumn1():
    return render_template('gameOfLife.html')

@app.route("/coreWar.html")
def twocolumn2():
    return render_template('coreWar.html')