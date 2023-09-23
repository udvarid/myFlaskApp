var speed = 500
var number = [0, 0, 0, 0]

function drawRectangle_(worms) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");    
    number = [0, 0, 0, 0]
    
    initCanvas()

    for (var i = 0; i < worms.length; i++) {
        const worm = JSON.parse(worms[i])
        const state = worm.state
        const color = worm.color
        fillUpColorTable(number, color)
        const direction = worm.direction
        ctx.fillStyle = color
        if (state == 'Egg') {            
            const egg_x = worm.coor_x - 1
            const egg_y = worm.coor_y - 1
            ctx.beginPath()
            ctx.ellipse(egg_x * 20 + 10, egg_y * 20 + 10, 5, 8, 90 * Math.PI/180, 0, 2 * Math.PI)    
            ctx.fill()        
        } else {            
            const bodies = worm.bodies
            var body_coordinates = []
            for (var j = 0; j < bodies.length; j++) {
                const body = bodies[j]
                const x = body.coor_x - 1
                const y = body.coor_y - 1
                body_coordinates.push([x, y])
            }
            for (var j = 0; j < bodies.length; j++) {
                const body = bodies[j]
                const x = body.coor_x - 1
                const y = body.coor_y - 1
                ctx.fillRect(x * 20 + 3, y * 20 + 3, 15, 15);
                //north neighbour
                const northCoor = y > 0 ? y - 1 : 39
                if (findCoordinate(body_coordinates, [x, northCoor])) {
                    ctx.fillRect(x * 20 + 3, y * 20, 15, 3);
                }
                //south neighbour
                const southCoor = y < 39 ? y + 1 : 0
                if (findCoordinate(body_coordinates, [x, southCoor])) {
                    ctx.fillRect(x * 20 + 3, y * 20 + 17, 15, 3);
                }
                //west neighbour
                const westCoor = x > 0 ? x - 1 : 39
                if (findCoordinate(body_coordinates, [westCoor, y])) {
                    ctx.fillRect(x * 20, y * 20 + 3, 3, 15);
                }
                //east neighbour
                const eastCoor = x < 39 ? x + 1 : 0
                if (findCoordinate(body_coordinates, [eastCoor, y])) {
                    ctx.fillRect(x * 20 + 17, y * 20 + 3, 3, 15);
                }

                if (body.body_type == 'B') {
                    ctx.fillStyle = "dark" + color
                    ctx.fillRect(x * 20 + 6, y * 20 + 6, 9, 9);
                    ctx.fillStyle = color
                }
                else if (body.body_type == 'M') {
                    ctx.fillStyle = "black"
                    if (direction == 'N') {
                        ctx.fillRect(x * 20 + 7, y * 20 + 3, 7, 11);
                    } else if (direction == 'W') {
                        ctx.fillRect(x * 20 + 3, y * 20 + 7, 11, 7);
                    } else if (direction == 'S') {
                        ctx.fillRect(x * 20 + 7, y * 20 + 7, 7, 11);
                    } else if (direction == 'E') {
                        ctx.fillRect(x * 20 + 7, y * 20 + 7, 11, 7);
                    }                     
                    ctx.fillStyle = color
                }
            }            
        }
    }
    write_report()
}

function fillUpColorTable(number, color) {
    if (color == 'red') {
        number[0] = number[0] + 1
    } else if (color == 'blue') {
        number[1] = number[1] + 1
    } else if (color == 'green') {
        number[2] = number[2] + 1
    } else if (color == 'orange') {
        number[3] = number[3] + 1
    }
}

function findCoordinate(bodies, body) {
    for (var j = 0; j < bodies.length; j++)  {        
        if (bodies[j][0] == body[0] && bodies[j][1] == body[1]) {
            return true
        }
    }
    return false
}

function changeSpeed(indicator) {    
    if (indicator == 1) {
        if (speed > 250) {
            speed = speed - 250
        } else if (speed > 100) {
            speed = 100
        } else if (speed == 100) {
            speed = 50
        }
    } else if (indicator == 2) {        
        if (speed == 50) {
            speed = 100
        } else if (speed == 100) {
            speed = 250
        } else if (speed < 1000) {
            speed = speed + 250
        }
    }
}

function startScripts() {
    initCanvas()
}

function initCanvas() {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");    
    const width = canvas.width;
    const height = canvas.height;    
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "black"
    ctx.fillRect(0, 0, width, height);    
    ctx.fillStyle = "red"
    ctx.fillRect(0, 0, width, 2);    
    ctx.fillRect(0, 0, 2, height);   
    ctx.fillRect(0, height - 2, width, height);         
    ctx.fillRect(width - 2, 0, width, height);
    ctx.fillStyle = "#292727"    
    for (var i = 1; i < 40; i++) {
        ctx.fillRect(2, i * 20, width - 4, 2);
        ctx.fillRect(i * 20, 2, 2, height - 4);
    }
}

async function stopSimulation() {        
    fetch('/stopsimulation_worm', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        });
}

function write_report() {        
    var tribe_1 = document.getElementById("tribe_1");
    var tribe_2= document.getElementById("tribe_2");
    var tribe_3 = document.getElementById("tribe_3");
    var tribe_4 = document.getElementById("tribe_4");
    tribe_1.textContent = number[0]    
    tribe_2.textContent = number[1]
    tribe_3.textContent = number[2]    
    tribe_4.textContent = number[3]    
}

function clean_report() {    
    var tribe_1 = document.getElementById("tribe_1");
    var tribe_2= document.getElementById("tribe_2");
    var tribe_3 = document.getElementById("tribe_3");
    var tribe_4 = document.getElementById("tribe_4");
    tribe_1.textContent = 0
    tribe_2.textContent = 0
    tribe_3.textContent = 0
    tribe_4.textContent = 0
} 

async function drawRectangle() {        
    fetch('/stopsimulation_worm', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.response == true) {          
                const worm_text_red = document.getElementById("worm_body_1").value         
                const worm_text_blue = document.getElementById("worm_body_2").value
                const worm_text_green = document.getElementById("worm_body_3").value
                const worm_text_orange = document.getElementById("worm_body_4").value
                const worm_text = worm_text_red + "_" + worm_text_blue + "_" + worm_text_green + "_" + worm_text_orange
                fetch("/startsimulation_worm/" + worm_text)
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        clean_report()
                    });                
            }
        });
    var stillRunning = true    
    while (stillRunning) {   
        const winner = checkWinner()
        if (winner != 0) {
            stillRunning = false            
        }
        await sleep(speed)      
        fetch("/getdata_worm")
            .then(response => response.json())
            .then(data => {                                       
                if (data.run == true) {                    
                    drawRectangle_(data.result)                            
                } else {
                    stillRunning = false                    
                }                
            })        
    }

}  

function checkWinner() {
    const sumOfWorms = number[0] + number[1] + number[2] + number[3]
    const limit = 0.75
    if (sumOfWorms == 0) {
        return 0
    }
    if (number[0] > 0 && number[0] / sumOfWorms >= limit) {
        return 1
    }
    if (number[1] > 0 && number[1] / sumOfWorms >= limit) {
        return 2
    }
    if (number[2] > 0 && number[2] / sumOfWorms >= limit) {
        return 3
    }
    if (number[3] > 0 && number[3] / sumOfWorms >= limit) {
        return 4
    }

    return 0
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function wormBody(worm) {
    var worm_text = document.getElementById("worm_body_" + worm);   
    const text_value = worm_text.value.toUpperCase()
    var final_text_value = ""
    for (let i in text_value) {
        if (["B","M","L","X"].includes(text_value[i])) {
            final_text_value += text_value[i]
        }
    }
    final_text_value = final_text_value.slice(0,12)
    if (final_text_value.length == 0) {
        final_text_value = "MBLXL"
    }
    worm_text.value = final_text_value
    worm_text.textContent = final_text_value    
}