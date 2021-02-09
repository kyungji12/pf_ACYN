//This javascript is for singlePose 
let video;
let poseNet;
let pose ;
let skeleton ; 

let brain;
let poseLabel = "";

let state = 'waiting';
let targetLabel;

function keyPressed(){
    if (key == 't') {
        brain.normalizeData();
        brain.train({
            epochs: 10
        }, finished);
    } else if (key == 's') {
        brain.saveData('test-data');
    } else {
        targetLabel = key;
        console.log(targetLabel);
        setTimeout(function(){
            console.log('collecting');
            state = 'collecting';
            setTimeout(function(){
                console.log('not collecting');
                state = 'waiting';
            },2000);
        },1000);
    }
}
function setup(){
    createCanvas(640, 480);
    video = createCapture(VIDEO);
    video.hide();
    poseNet = ml5.poseNet(video, modelLoaded);
    poseNet.on('pose', gotPoses);

    let options = {
        inputs: 34,
        outputs: 1,
        task: 'classification',
        debug: true
    }
    brain = ml5.neuralNetwork(options);
}

function brainLoaded(){
    console.log('pose classification ready');
    classifyPose();
}
function classifyPose(){
    if (pose){
        let inputs = [];
        for (let i = 0; i < pose.keypoints.length; i++) {
            let keypoint = pose.keypoints[i];
            let X = keypoint.position.x;
            let Y = keypoint.position.y;
            inputs.push(X);
            inputs.push(Y);
        }
        brain.classfiy(inputs, gotResult);
    } else {
        setTimeout(classifyPose, 100);
    }
}
function gotResult(error, results) {
    if (results[0].confidence > 0.75){
        poseLabel = results[0].label.toUpperCase();
    }
    classifyPose();
}

function dataReady(){
    brain.normalizeData();
    brain.train({
        epochs: 10
    }, finished);
}
function finished(){
    console.log('model trained');
    brain.save();
    classifyPose();
}
function gotPoses(poses){
    // console.log(poses);
    if (poses.length > 0) {
        pose = poses[0].pose;
        skeleton = poses[0].skeleton;
        if (state == 'collecting') {
            let inputs = [];
            for (let i = 0; i < pose.keypoints.length; i++) {
                let keypoint = pose.keypoints[i];
                let X = keypoint.position.x;
                let Y = keypoint.position.y;
                inputs.push(X);
                inputs.push(Y);
            }
            // let target = [targetLabel];
            let outputs = [];
            outputs = inputs;
            brain.addData(inputs, outputs);
            // console.log(i,"💜",inputs);
        }
    }
}
function modelLoaded(){
    console.log("poseNet ready");
    // poseNet.singlePose(video);
}
function draw(){
    push();
    translate(video.width, 0);
    scale(-1, 1);
    image(video, 0, 0, video.width, video.height);

    drawKeypoints();
    drawSkeleton();
    pop();
}

function drawKeypoints(){
    //console.log("drawKeypoints");
        if (pose) {
            for (let i = 0; i < pose.keypoints.length; i ++) {
                let keypoint = pose.keypoints[i];
                let X = keypoint.position.x;
                let Y = keypoint.position.y;
                if (keypoint.score > 0.2) {
                    // ctx.fillStyle = 'lavender';
                    // ctx.beginPath();
                    // ctx.arc(X,Y, 10, 0, 2*Math.PI);
                    // ctx.fill();
                    fill('lavender');
                    stroke('lavender');
                    ellipse(X, Y, 16, 16);
                }
            }
        }
    }
    function drawSkeleton() {
    //console.log("drawSkeleton");
        if (skeleton) {
            for (let i = 0; i < skeleton.length; i ++) {
                let partA = skeleton[i][0];
                let partB = skeleton[i][1];
                // ctx.strokeStyle = 'lavender';
                // ctx.lineWidth = 2;
                // ctx.beginPath();
                // ctx.moveTo(partA.position.x, partA.position.y);
                // ctx.lineTo(partB.position.x, partB.position.y);
                // // ctx.lineTo(partA.position.x, partA.position.y, partB.position.x, partB.position.y);
                // ctx.stroke();
                strokeWeight(2);
                stroke('lavender');
                line(partA.position.x, partA.position.y, partB.position.x, partB.position.y);
            }
        }
    }