//IMAGE PROCESSOR
//Elements
const set__sensivility = document.getElementsByClassName('set__sensivility')[0];
const set__barError = document.getElementsByClassName('set__bar')[1];
const set__textError = document.getElementsByClassName('set__textError')[0];

const img1 = document.getElementsByClassName('img1')[0];
const img2 = document.getElementsByClassName('img2')[0];
const canvas1 = document.getElementsByClassName('canvasImg1')[0];
const canvas2 = document.getElementsByClassName('canvasImg2')[0];

//Sensivility default value
let senValue;
//Control Boolean
let nonErrors;
//Errors Container
let errorsArray = [];
//Images input from json
fetch('inputs.json')
    .then()
    .then()
    .catch()
//Events
set__sensivility.addEventListener('click', function () {
    processor.doLoad();
})

addEventListener('resize', function () {
    processor.doLoad();
})

addEventListener('load', function () {
    processor.doLoad();
})


//processor object
processor = {}

processor.doLoad = function doLoad() {
    checkPromises ();

    if (nonErrors) {
        senValue = set__sensivility.value;

        this.img1 = img1;
        this.img2 = img2;

        this.canvas = canvas1;
        this.ctx = this.canvas.getContext('2d');

        this.canvas2 = canvas2;
        this.ctx2 = this.canvas2.getContext('2d');

        this.width = window.innerWidth / 3;
        this.heigth = this.width * (this.img1.naturalHeight / this.img1.naturalWidth);

        this.canvas.width = this.width;
        this.canvas.height = this.heigth;

        this.canvas2.width = this.width;
        this.canvas2.height = this.heigth;
        this.canvas2.style.display = 'none';

        this.computeFrame();
    }
}

processor.computeFrame = function computeFrame() {
    this.ctx.drawImage(this.img1, 0, 0, this.width, this.heigth);
    const frameOne = this.ctx.getImageData(0, 0, this.width, this.heigth);
    this.frameOne = frameOne;
    this.ctx2.drawImage(this.img2, 0, 0, this.width, this.heigth);
    const frameTwo = this.ctx2.getImageData(0, 0, this.width, this.heigth);
    this.frameTwo = frameTwo;
    //Getting rgb per pixel of the image 1
    for (let i = 0; i < this.frameOne.data.length; i += 4) {
        const redImageOne = this.frameOne.data[i + 0];
        const greenImageOne = this.frameOne.data[i + 1];
        const blueImageOne = this.frameOne.data[i + 2];
        //Getting rgb per pixel of the image 2
        if (this.frameTwo != undefined && this.frameTwo != null && this.frameTwo != NaN ) {
            const redImageTwo = this.frameTwo.data[i + 0];
            const greenImageTwo = this.frameTwo.data[i + 1];
            const blueImageTwo = this.frameTwo.data[i + 2];
            //Comparing rgb per pixel between images and highlighting with red. Logaritmic scale is used.
            const sensibility = senValue / 100;
            if (Math.log((redImageOne-redImageTwo) ** 2) > sensibility || Math.log((greenImageOne-greenImageTwo) ** 2) > sensibility || Math.log((blueImageOne-blueImageTwo) ** 2) > sensibility) {
                this.frameOne.data[i + 0] = 255;
                this.frameOne.data[i + 1] = 0;
                this.frameOne.data[i + 2] = 0;
            }
        }
    }
    this.ctx.putImageData(frameOne, 0, 0);
}

//Promises

function isImageOne () {
    return new Promise (function (resolve, reject) {
        if (img1.naturalHeight != 0 && img1.naturalWidth != 0 && img1.getAttribute('src') != '') {
            resolve();
        } else {
            reject ([false, "Error: There is an error on the image one. Please check if you added an image."]);
        }
    })
}

function isImageTwo () {
    return new Promise (function (resolve, reject) {
        if (img2.naturalHeight != 0 && img2.naturalWidth != 0 && img2.getAttribute('src') != '') {
            resolve();
        } else {
            reject ([false, "Error: There is an error on the image two. Please check if you added an image."]);
        }
    })
}

function checkPromises () {
    nonErrors = true;
    isImageOne().then (
        function () {
            set__barError.style.display = 'none';
            return isImageTwo();
        }
    ).then (
        function () {
            set__barError.style.display = 'none';
        }
    ).catch (
        function (e) {
            nonErrors =  e[0];
            printErrors(e)
        }
    )
}

//printErrors

function printErrors(error) {
    errorsArray.push(error);
    let errorMessage
    for (let i = 0; i < errorsArray.length; i++){
        errorMessage += errorsArray[i] + '<br>';
    }
    set__barError.style.display = 'block';
    set__textError.innerText = errorMessage;
}