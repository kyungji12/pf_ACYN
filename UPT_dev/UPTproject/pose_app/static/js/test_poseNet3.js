//This javascript is for singlePose 

let canvas = document.getElementById("canvas");
let video = document.getElementById("video");
let ctx = canvas.getContext("2d");
let poseNet;
let pose ;
let skeleton ; 

let brain;
let poseLabel = "";

let state = 'waiting';
let targetLabel;

// let stopBtn = document.getElementsById("stopBtn");

// create video
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
      video.srcObject = stream;
      video.play();
    });
}

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
            },1000);
        },1000);
    }
}

function drawCameraIntoCanvas(){ //setUp()
    ctx.drawImage(video, 0,0, 640, 480);

    draw();
    // drawKeypoints();
    // drawSkeleton();

    window.requestAnimationFrame(drawCameraIntoCanvas);
    
    let options = {
        inputs: 34, //17개의 부위 x,y 각 두개씩 -> 총 34개
        outputs: 34, //플랭크포즈 1개
        task: 'classification',
        debug: true
    }
    brain = ml5.neuralNetwork(options);

    // brain.loadData('test.json', dataReady);
}
drawCameraIntoCanvas();
poseNet = ml5.poseNet(video, modelReady);
poseNet.on('pose', gotPoses);

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
            let target = [targetLabel];
            brain.addData(inputs, inputs);
            // console.log(i,"💜",inputs);
        }
    }
}
function modelReady(){
    console.log("model ready");
    poseNet.singlePose(video);
}
function draw(){
    // push();
    // translate(video.width, 0);
    // scale(-1, 1);
    // ctx.drawImage(video, 0, 0, video.width, video.height);

    if (pose) { 
        for (let i = 0; i < pose.keypoints.length; i++) {
            let keypoint = pose.keypoints[i];
            let X = keypoint.position.x;
            let Y = keypoint.position.y;
            if (keypoint.score > 0.2) {
                ctx.fillStyle = 'lavender';
                ctx.beginPath();
                ctx.arc(X,Y, 10, 0, 2*Math.PI);
                ctx.fill();
            }
        }
    }
    if (skeleton) {
        for (let i = 0; i < skeleton.length; i++) {
            let partA = skeleton[i][0];
            let partB = skeleton[i][1];
            ctx.strokeStyle = 'lavender';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(partA.position.x, partA.position.y);
            ctx.lineTo(partB.position.x, partB.position.y);
            // ctx.lineTo(partA.position.x, partA.position.y, partB.position.x, partB.position.y);
            ctx.stroke();
        }
    }
    // pop();
}
// function drawKeypoints(){
//     if (pose) { 
//         for (let i = 0; i < pose.keypoints.length; i++) {
//             let keypoint = pose.keypoints[i];
//             let X = keypoint.position.x;
//             let Y = keypoint.position.y;
//             if (keypoint.score > 0.2) {
//                 ctx.fillStyle = 'lavender';
//                 ctx.beginPath();
//                 ctx.arc(X,Y, 10, 0, 2*Math.PI);
//                 ctx.fill();
//             }
//         }
//     }
// }
// function drawSkeleton() {
//     if (skeleton) {
//         for (let i = 0; i < skeleton.length; i++) {
//             let partA = skeleton[i][0];
//             let partB = skeleton[i][1];
//             ctx.strokeStyle = 'lavender';
//             ctx.lineWidth = 2;
//             ctx.beginPath();
//             ctx.moveTo(partA.position.x, partA.position.y);
//             ctx.lineTo(partB.position.x, partB.position.y);
//             // ctx.lineTo(partA.position.x, partA.position.y, partB.position.x, partB.position.y);
//             ctx.stroke();
//         }
//     }
// }