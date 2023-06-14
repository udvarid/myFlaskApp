function drawRectangle_(cells) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");    
    
    const width = canvas.width;
    const height = canvas.height;    
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "black"
    ctx.fillRect(0, 0, width, height);    

    for (var i = 0; i < cells.length; i++) {
        console.log(cells[i])
        const x = JSON.parse(cells[i]).x
        const y = JSON.parse(cells[i]).y
        const value = JSON.parse(cells[i]).value
        console.log(x, y, value)
        ctx.fillStyle = "red"
        ctx.fillRect(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20);                    
    }
  }

async function drawRectangle() {        
    fetch('/stopsimulation', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        });
    const players = document.getElementById("players").value;
    const initCells = document.getElementById("initCells").value;
    fetch("/startsimulation/" + players + "/" + initCells)
        .then(response => response.json())
        .then(data => {
            console.log(data)        
        });
    await sleep(1000)      
    for (let i = 0; i < 1; i++) {        
        fetch("/getdata")
            .then(response => response.json())
            .then(data => {                
                drawRectangle_(data.result)        
            })
        await sleep(1000)      
    }
}  

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}