//Images input from json
async function drawHTML(){
    await fetch('inputs.json')
        .then(res => res.json())
        .then(res => generateHTML(res))
        .catch(e => console.log(e));
}

function createSetBar(name){
    const sec = document.createElement('SECTION');
    sec.classList.add('set');
    sec.innerHTML = `
        <div class="set__bar">
            <div class="set__name">${name}</div>
            <label class="set__text" for="sensibility">sensibility</label>
            <input class="set__sensibility" id="sensibility" type="range" min="0" max="1000" value="500">
        </div>
        <div class="set__bar set__errorBar" style="display:none">
            <p class="set__textError"></p>
        </div>
    `;
    return sec;
}

function createPair(path1, path2){
    const sec = document.createElement('SECTION');
    sec.classList.add('resource');
    sec.innerHTML = `
        <div class='resource__img'>
                <img class='img1' src='${path1}'>
            </div>
            <div class='resource__img'>
                <img class='img2' src='${path2}'>
            </div>
            <div class='resource__canvas resource__canvas--visible'>
                <canvas class='canvasImg1' width='' height=''></canvas>
            </div>
            <div class="resource__canvas">
                <canvas class='canvasImg2' width='' height=''></canvas>
        </div>
    `;
    return sec;
}

function generateHTML(data){
    const fragment = document.createDocumentFragment();

    for(const pair of Object.entries(data)){
        fragment.appendChild(createSetBar(pair[1][2]));
        fragment.appendChild(createPair(pair[1][0], pair[1][1]));
    }
    document.getElementById("body").appendChild(fragment)
}




