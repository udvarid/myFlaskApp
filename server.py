from flask import Flask, render_template
from gameOfLife import GameOfLifeBrain

brain = GameOfLifeBrain()
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

@app.route("/stopsimulation")
def stopsimulation():
    brain.stop_simulation()
    return {"response" : True}

@app.route("/startsimulation/<int:players>/<int:initcells>")
def startsimulation(players, initcells):    
    params = {
        'size': 40,
        'players': players,
        'init_cells': initcells
    }
    brain.run_simulation(params)
    return {"response" : True}


@app.route("/getdata")
def me_api():     

    return {
        "username": "Donát",
        "age": "44",
        "run": brain.run_check()
    }