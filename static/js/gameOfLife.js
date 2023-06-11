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
    for (let i = 0; i < 10; i++) {
        drawRectangle_()
        await sleep(1000)      
    }
}  

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}