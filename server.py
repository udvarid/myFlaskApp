import json
from flask import Flask, render_template
from gameOfLife import GameOfLifeBrain
from wormBrain import WormBrain
from worm import BodyType

brain = GameOfLifeBrain()
worm = WormBrain()
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

@app.route("/wormsWar.html")
def twocolumn2():
    return render_template('wormsWar.html')

@app.route("/stopsimulation")
def stopsimulation():
    brain.stop_simulation()
    return {"response" : True}

@app.route("/stopsimulation_worm")
def stopsimulation_worm():
    worm.stop_simulation()
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

@app.route("/startsimulation_worm")
def startsimulation_worm():    
    # TODO egyenlőre 2 constanst prototípust rakjunk össze, később ezt és az egyéb paramétereket kapja
    body_types_red = [BodyType.MOUTH, BodyType.BRAIN, BodyType.LEG, BodyType.MULTIPLIER, BodyType.LEG]
    body_types_blue = [BodyType.MOUTH, BodyType.BRAIN, BodyType.LEG, BodyType.MULTIPLIER, BodyType.LEG]
    params = {
        'size': 40,
        'worm_red': {
            'body_type': body_types_red
        },
        'worm_blue': {
            'body_type': body_types_blue
        }
    }
    worm.run_simulation(params)    
    return {"response" : True}


@app.route("/getdata")
def me_api():     
    still_running = brain.run_check()    
    result = [] if not still_running else brain.ask_next_result()       
    return {
        "run": still_running,
        "result": [json.dumps(u.__dict__) for u in result]
    }

@app.route("/getdata_worm")
def me_api_worm():     
    still_running = worm.run_check()
    result = [] if not still_running else worm.ask_next_result()        
    return {
        "run": still_running,
        "result": [json.dumps(u.__dict__) for u in result]
    }