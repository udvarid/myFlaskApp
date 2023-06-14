function drawRectangle_(cells) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");    
    
    initBlack()

    for (var i = 0; i < cells.length; i++) {        
        const x = JSON.parse(cells[i]).x
        const y = JSON.parse(cells[i]).y
        const value = JSON.parse(cells[i]).value        
        if (value == 1) {
            ctx.fillStyle = "red"    
        } else if (value == 2) {
            ctx.fillStyle = "blue"    
        } else if (value == 3) {
            ctx.fillStyle = "green"    
        } else if (value == 4) {
            ctx.fillStyle = "yellow"    
        }
        
        ctx.fillRect(x * 20 + 1, y * 20 + 1, 18, 18);                    
    }
  }

function initBlack() {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");    
    const width = canvas.width;
    const height = canvas.height;    
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "black"
    ctx.fillRect(0, 0, width, height);    
}

async function stopSimulation() {        
    fetch('/stopsimulation', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        });
}
  

async function drawRectangle() {        
    fetch('/stopsimulation', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.response == true) {
                const players = document.getElementById("players").value;
                const initCells = document.getElementById("initCells").value;
                fetch("/startsimulation/" + players + "/" + initCells)
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)        
                    });                
            }
        });
    var stillRunning = true
    while (stillRunning) {
        await sleep(500)      
        fetch("/getdata")
            .then(response => response.json())
            .then(data => {          
                console.log(data)              
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