let tribe_buttons = document.getElementsByClassName("btn_tribes");
let init_buttons = document.getElementsByClassName("btn_init");
var number_of_tribes = 4
var number_of_inits = 4
selectTribeButton(4)
selectInitButton(4)

function selectTribeButton(index) {    
    for (let i = 0; i < tribe_buttons.length; i++) {
        tribe_buttons[i].classList.remove("selected");
    }    
    
    tribe_buttons[index - 1].classList.add("selected");    
  }

function selectInitButton(index) {    
    for (let i = 0; i < init_buttons.length; i++) {
        init_buttons[i].classList.remove("selected");
    }    
    
    init_buttons[index - 1].classList.add("selected");
    number_of_inits = index
}  

function drawRectangle_(cells) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const number = [0, 0, 0, 0]    
    
    initCanvas()

    for (var i = 0; i < cells.length; i++) {        
        const x = JSON.parse(cells[i]).x
        const y = JSON.parse(cells[i]).y
        const value = JSON.parse(cells[i]).value        
        if (value == 1) {
            ctx.fillStyle = "red"    
            number[0] = number[0] + 1
        } else if (value == 2) {
            ctx.fillStyle = "blue"   
            number[1] = number[1] + 1 
        } else if (value == 3) {
            ctx.fillStyle = "green"  
            number[2] = number[2] + 1  
        } else if (value == 4) {
            ctx.fillStyle = "yellow" 
            number[3] = number[3] + 1   
        }        
        write_report(number)
        
        ctx.fillRect(x * 20 + 1, y * 20 + 1, 18, 18);                    
    }
  }

function write_report(number) {        
    var tribe_1 = document.getElementById("tribe_1");
    var tribe_2= document.getElementById("tribe_2");
    var tribe_3 = document.getElementById("tribe_3");
    var tribe_4 = document.getElementById("tribe_4");
    tribe_1.textContent = number[0]    
    if (number_of_tribes > 1) {
        tribe_2.textContent = number[1]
    }    
    if (number_of_tribes > 2) {
        tribe_3.textContent = number[2]    
    }
    if (number_of_tribes > 3) {
        tribe_4.textContent = number[3]    
    }
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

    var tribe_all_1 = document.getElementById("tribe_all_1");
    var tribe_all_2 = document.getElementById("tribe_all_2");
    var tribe_all_3 = document.getElementById("tribe_all_3");
    var tribe_all_4 = document.getElementById("tribe_all_4");
    tribe_all_1.style.display = ""
    if (number_of_tribes > 1) {
        tribe_all_2.style.display = ""
    } else {
        tribe_all_2.style.display = "none"    
    }    
    if (number_of_tribes > 2) {
        tribe_all_3.style.display = ""
    } else {
        tribe_all_3.style.display = "none"    
    }    
    if (number_of_tribes > 3) {
        tribe_all_4.style.display = ""
    } else {
        tribe_all_4.style.display = "none"    
    }    
}

function startScripts() {
    initCanvas()
    var tribe_all_1 = document.getElementById("tribe_all_1");
    var tribe_all_2 = document.getElementById("tribe_all_2");
    var tribe_all_3 = document.getElementById("tribe_all_3");
    var tribe_all_4 = document.getElementById("tribe_all_4");
    tribe_all_1.style.display = "none"
    tribe_all_2.style.display = "none"
    tribe_all_3.style.display = "none"
    tribe_all_4.style.display = "none"
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
                let selectedTribes = -1;                
                for (let i = 0; i < tribe_buttons.length; i++) {
                    if (tribe_buttons[i].classList.contains("selected")) {
                        selectedTribes = i + 1;
                      break;
                    }
                }      
                number_of_tribes = selectedTribes        
                fetch("/startsimulation/" + selectedTribes + "/" + number_of_inits * 10)
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)        
                        clean_report()
                    });                
            }
        });
    var stillRunning = true
    while (stillRunning) {
        await sleep(500)      
        fetch("/getdata")
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