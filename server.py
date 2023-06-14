from flask import Flask, render_template, jsonify
from gameOfLife import GameOfLifeBrain, Cell
import json

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
    still_running = brain.run_check()    
    result = [] if not still_running else brain.ask_next_result()       
    return {
        "run": still_running,
        "result": [json.dumps(u.__dict__) for u in result]
    }