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

@app.route("/startsimulation_worm/<string:worm_text>")
def startsimulation_worm(worm_text):
    separated_worm_bodies = worm_text.split("_")
    body_types_red = list(map(get_worm_body_type, [body_char for body_char in separated_worm_bodies[0]]))
    body_types_blue = list(map(get_worm_body_type, [body_char for body_char in separated_worm_bodies[1]]))
    body_types_green = list(map(get_worm_body_type, [body_char for body_char in separated_worm_bodies[2]]))
    body_types_yellow = list(map(get_worm_body_type, [body_char for body_char in separated_worm_bodies[3]]))
    params = {
        'size': 40,
        'worm_red': {
            'body_type': body_types_red
        },
        'worm_blue': {
            'body_type': body_types_blue
        },
        'worm_green': {
            'body_type': body_types_green
        },
        'worm_yellow': {
            'body_type': body_types_yellow
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

def get_worm_body_type(body_char):
    if (body_char == "M"):
        return BodyType.MOUTH
    elif (body_char == "B"):
        return BodyType.BRAIN
    elif (body_char == "L"):
        return BodyType.LEG
    elif (body_char == "X"):
        return BodyType.MULTIPLIER