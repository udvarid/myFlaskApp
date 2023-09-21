function drawRectangle_(worms) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");    
    
    initCanvas()

    for (var i = 0; i < worms.length; i++) {
        const worm = JSON.parse(worms[i])
        const state = worm.state
        const color = worm.color
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
}

function findCoordinate(bodies, body) {
    for (var j = 0; j < bodies.length; j++)  {        
        if (bodies[j][0] == body[0] && bodies[j][1] == body[1]) {
            return true
        }
    }
    return false
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
  

async function drawRectangle() {        
    fetch('/stopsimulation_worm', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.response == true) {                
                fetch("/startsimulation_worm")
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)                               
                    });                
            }
        });
    var stillRunning = true    
    while (stillRunning) {        
        await sleep(500)      
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

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}