main()

//IMAGE PROCESSOR
async function main(){
    await drawHTML();
    closeServer();
    //Elements
    const set__sensivility = document.getElementsByClassName('set__sensivility');
    const set__barError = document.getElementsByClassName('set__errorBar');
    const set__textError = document.getElementsByClassName('set__textError');
    const images1 = document.getElementsByClassName('img1');
    const images2 = document.getElementsByClassName('img2');
    const canvas1 = document.getElementsByClassName('canvasImg1');
    const canvas2 = document.getElementsByClassName('canvasImg2');

    //Events
    for (let i = 0; i < images1.length; i++){
        let a = i
        images1[a].addEventListener('load', function () {
            runProcess(a);
        });
        images2[a].addEventListener('load', function () {
            runProcess(a);
        });
        set__sensivility[a].addEventListener('click', function () {
            runProcess(a);
        });
    }

    addEventListener('resize', function () {
        for (let i = 0; i < images1.length; i++){
            runProcess(i);
        }
    });

    closeServer();

    //Signal to close the server
    function closeServer(){
        url =  window.location.hostname
        fetch(url, {
            method: 'CLOSE'
        })
    }
    //Process set function
    function process(i){
        let width = window.innerWidth / 3;
        let height = width * (images1[i].naturalHeight / images1[i].naturalWidth);
        canvas1[i].width = width;
        canvas1[i].height = height;
        canvas2[i].width = width;
        canvas2[i].height = height;
        let c1 = new canvas(canvas1[i], width, height);
        let c2 = new canvas(canvas2[i], width, height);
        let p = new processor(images1[i], images2[i], c1, c2);
        p.senValue = set__sensivility[i].value;
        p.computeFrame();
    }

    //Run process() when promises are resolved
    function runProcess(i){
        isImageOne(i).then (
            function() {
                set__barError[i].style.display = 'none';
                return isImageTwo(i);
            }
        ).then (
            function() {
                set__barError[i].style.display = 'none';
                process(i);
            }
        ).catch (
            function(e) {
                printErrors(e, i);
            }
        )
    }

    //Promises definition
    function isImageOne (i) {
        return new Promise (function (resolve, reject) {
            if (images1[i].naturalHeight != 0 && images1[i].naturalWidth != 0 && images1[i].getAttribute('src') != '') {
                resolve();
            } else {
                reject ("Error: There is an error on the image one. Please check if you added an image.");
            }
        });
    }

    function isImageTwo (i) {
        return new Promise (function (resolve, reject) {
            if (images2[i].naturalHeight != 0 && images2[i].naturalWidth != 0 && images2[i].getAttribute('src') != '') {
                resolve();
            } else {
                reject ("Error: There is an error on the image two. Please check if you added an image.");
            }
        });
    }
    //Error display
    function printErrors(error, i) {
        set__barError[i].style.display = 'block';
        set__textError[i].innerText = error;
    }
}

//Canvas class
class canvas {
    constructor(canvas, width, heigth) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = width;
        this.heigth = heigth;
    }

    getFrame(img) {
        this.ctx.drawImage(img, 0, 0, this.width, this.heigth);
        return this.ctx.getImageData(0, 0, this.width, this.heigth);
    }
}

//processor class
class processor {
    constructor(img1, img2, canvas1, canvas2) {
        this.img1 = img1;
        this.img2 = img2;
        this.canvas1 = canvas1;
        this.canvas2 = canvas2;
        this.senValue = 500;
    }

    computeFrame() {
        const frameOne = this.canvas1.getFrame(this.img1);
        const frameTwo = this.canvas2.getFrame(this.img2);
        //Getting rgb per pixel of the image 1
        for (let i = 0; i < frameOne.data.length; i += 4) {
            const redImageOne = frameOne.data[i + 0];
            const greenImageOne = frameOne.data[i + 1];
            const blueImageOne = frameOne.data[i + 2];
            //Getting rgb per pixel of the image 2
            if (frameTwo != undefined && frameTwo != null && frameTwo != NaN ) {
                const redImageTwo = frameTwo.data[i + 0];
                const greenImageTwo = frameTwo.data[i + 1];
                const blueImageTwo = frameTwo.data[i + 2];
                //Comparing rgb per pixel between images and highlighting with red. Logaritmic scale is used.
                const sensibility = (1000 - this.senValue) / 100;
                if (Math.log((redImageOne-redImageTwo) ** 2) > sensibility || Math.log((greenImageOne-greenImageTwo) ** 2) > sensibility || Math.log((blueImageOne-blueImageTwo) ** 2) > sensibility) {
                    frameOne.data[i + 0] = 255;
                    frameOne.data[i + 1] = 0;
                    frameOne.data[i + 2] = 0;
                }
            }
        }
        this.canvas1.ctx.putImageData(frameOne, 0, 0);
    }
}