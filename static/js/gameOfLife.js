function drawRectangle_() {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    
    const width = 800;
    const height = 800;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < width / 20; i++) {
        for (let j = 0; j < height / 20; j++) {
            const myRand = Math.random()
            if (myRand < 0.1) {
                ctx.fillStyle = "red";    
            } else if (myRand < 0.2) {
                ctx.fillStyle = "blue";    
            } else {
                ctx.fillStyle = "black";    
            }
            ctx.fillRect(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20);                    
        }
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
    for (let i = 0; i < 10; i++) {
        //drawRectangle_()        
        fetch("/getdata")
            .then(response => response.json())
            .then(data => {
                console.log(data)
            })
        await sleep(1000)      
    }
}  

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}