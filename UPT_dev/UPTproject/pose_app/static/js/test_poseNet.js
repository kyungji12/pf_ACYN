// // This javascript is for multiPose
// let canvas = document.getElementById("canvas");
// let video = document.getElementById("video");
// let ctx = canvas.getContext("2d");

// let poses = [];

// // create video
// if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//     navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
//       video.srcObject = stream;
//       video.play();
//     });
//     //   navigator.mediaDevices.getUserMedia({ video: false }).catch(function(err) {
//     //   // 오류 처리
//     //   alert("비디오 권한을 사용하지 않으면 UPT 서비스를 이용할 수 없습니다.");
//     // });
//   }

// //그림을 그릴 수 있는 canvas안에 video 위치시키기
// function drawCameraIntoCanvas(){
// // draw the video element into the canvas
//     ctx.drawImage(video, 0,0, 640, 480);
// // We can call both functions to draw all keypoints and the skeletons
//     drawKeypoints();
//     drawSkeleton();

//     window.requestAnimationFrame(drawCameraIntoCanvas);
// }
// //Loop over the drawCameraIntoCanvas function
// drawCameraIntoCanvas();

// //Create a new poseNet methode with a single detection 
// let poseNet = ml5.poseNet(video, modelReady);
// //An event listener that returns the results when a pose is detected. 
// poseNet.on('pose', gotPoses);

// // poseNet.on('pose', (results) => {
// //     // do something with the results
// //     console.log(results);
// // });

// //A function that gets called every time there's an update from the model
// function gotPoses(results){
//     //console.log(results);
//     poses = results;
// }
// function modelReady(){
//     console.log("model ready");
//     // poseNet.singlePose(video);
//     poseNet.multiPose(video);
// }
// // A function to draw ellipses over the detected keypoints
// function drawKeypoints(){
// //console.log("drawKeypoints");
// //Loop through all the poses detected
//     for (let i = 0; i < poses.length; i += 1) {
//     // For each pose detected, loop through all the keypoints
//         for (let j = 0; j < poses[i].pose.keypoints.length; j += 1) {
//             let keypoint = poses[i].pose.keypoints[j];
//             let X = keypoint.position.x;
//             let Y = keypoint.position.y;
//             //Only draw an ellipse is the pose probability is bigger than 0.2
//         if (keypoint.score > 0.2) {
//                 ctx.fillStyle = 'lavender';
//             //Call this method when you want to create a new path
//                 ctx.beginPath();
//             //draw circle
//                 ctx.arc(X, Y, 10, 0, 2 * Math.PI);
//             //outline
//                 ctx.fill(); 
//             }
//         }
//     }
// }
// // A function to draw the skeletons
// function drawSkeleton() {
// //console.log("drawSkeleton");
// //Loop throuth all the skeletons detected
//     for (let i = 0; i < poses.length; i += 1) {
//     // For every skeleton, loop through all body connections
//         for (let j = 0; j < poses[i].skeleton.length; j += 1) {
//             let partA = poses[i].skeleton[j][0];
//             let partB = poses[i].skeleton[j][1];
//             ctx.strokeStyle = 'lavender';
//             ctx.lineWidth = 2;
//             ctx.beginPath();
//             ctx.moveTo(partA.position.x, partA.position.y);
//             ctx.lineTo(partB.position.x, partB.position.y);
//             ctx.stroke();
//         }
//     }
// }

// // function draw() {
// //     var canvas = document.getElementById('canvas');
// //     if (canvas.getContext) {
// //         var ctx = canvas.getContext('2d');

// //         var rectangle = new Path2D();
// //         rectangle.rect(10, 10, 50, 50);

// //         var circle = new Path2D();
// //         circle.moveTo(125, 35);
// //         circle.arc(100, 35, 25, 0, 2 * Math.PI);

// //         ctx.stroke(rectangle);
// //         ctx.fill(circle);
// //     }
// // }




// ////////////////////////////////////////////////////////////////
// let canvas = document.getElementById("canvas");
// let video = document.getElementById("video");
// let ctx = canvas.getContext("2d");

// let pose ;
// let skeleton ; 

// let brain;
// let poseLabel = "";

// let state = 'waiting';
// let targetLabel;

// if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//     navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
//       video.srcObject = stream;
//       video.play();
//     });
// }
// function keyPressed(){
//     if (key == 't') {
//         brain.normalizeData();
//         brain.train({
//             epochs: 10
//         }, finished);
//     } else if (key == 's') {
//         brain.saveData('test-data');
//     } else {
//         targetLabel = key;
//         console.log(targetLabel);
//         setTimeout(function(){
//             console.log('collecting');
//             state = 'collecting';
//             setTimeout(function(){
//                 console.log('not collecting');
//                 state = 'waiting';
//             },2000);
//         },1000);
//     }
// }

// function setup(){
//     // video.hide();
//     let poseNet = ml5.poseNet(video, modelReady);
//     poseNet.on('pose', gotPoses);

//     let options = {
//         inputs: 34,
//         outputs: 1,
//         task: 'classification',
//         debug: true
//     }
//     brain = ml5.neuralNetwork(options);
// }
// // function drawCameraIntoCanvas(){
// //     ctx.translate(video.width, 0);
// //     ctx.scale(-1, 1);
// //     ctx.drawImage(video, 0,0, 640, 480);
// //     window.requestAnimationFrame(drawCameraIntoCanvas);
// // }
// // drawCameraIntoCanvas();

// // let poseNet = ml5.poseNet(video, modelReady);
// // poseNet.on('pose', gotPoses);
// function brainLoaded(){
//     console.log('pose classification ready');
//     classifyPose();
// }
// function classifyPose(){
//     if (pose){
//         let inputs = [];
//         for (let i = 0; i < pose.keypoints.length; i++) {
//             let keypoint = pose.keypoints[i];
//             let X = keypoint.position.x;
//             let Y = keypoint.position.y;
//             inputs.push(X);
//             inputs.push(Y);
//         }
//         brain.classfiy(inputs, gotResult);
//     } else {
//         setTimeout(classifyPose, 100);
//     }   
// }
// function gotResult(error, results) {
//     if (results[0].confidence > 0.75){
//         poseLabel = results[0].label.toUpperCase();
//     }
//     classifyPose();
// }

// function dataReady(){
//     brain.normalizeData();
//     brain.train({
//         epochs: 10
//     }, finished);
// }
// function finished(){
//     console.log('model trained');
//     brain.save();
//     classifyPose();
// }
// function gotPoses(poses){
//     // console.log(poses);
//     if (poses.length > 0) {
//         pose = poses[0].pose;
//         skeleton = poses[0].skeleton;
//         if (state == 'collecting') {
//             let inputs = [];
//             for (let i = 0; i < pose.keypoints.length; i++) {
//                 let keypoint = pose.keypoints[i];
//                 let X = keypoint.position.x;
//                 let Y = keypoint.position.y;
//                 inputs.push(X);
//                 inputs.push(Y);
//             }
//             // let target = [targetLabel];
//             let outputs = [];
//             outputs = inputs;
//             brain.addData(inputs, outputs);
//             // console.log(i,"💜",inputs);
//         }
//     }
// }
// function modelReady(){
//     console.log("model ready");
//     // poseNet.singlePose(video);
// }
// function draw(){
//     // drawCameraIntoCanvas();
//     // push();
//     // console.log(video.width);
//     ctx.save();
//     ctx.scale(-1, 1);
//     ctx.translate(-video.width, 0);
//     ctx.drawImage(video, 0,0, 640, 480);
//     drawKeypoints();
//     drawSkeleton();
//     ctx.restore();
//     // pop();
// }
// function drawKeypoints(){
//     if (pose) { 
//         for (let i = 0; i < pose.keypoints.length; i ++) {
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
//         for (let i = 0; i < skeleton.length; i ++) {
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



////사실 neural network는 필요없이 ajax로 result 보내면 끝/////////////////////////////////////////////
//This javascript is for singlePose 
let canvas = document.getElementById("canvas");
let video = document.getElementById("video");
let ctx = canvas.getContext("2d");

let pose ;
let skeleton ; 

let brain;
let poseLabel = "";

let state = 'waiting';
let targetLabel;

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
      video.srcObject = stream;
      video.play();
    });
}

let readySection = document.getElementById("readySection");
let workoutSection = document.getElementById("workoutSection");
let stopSection = document.getElementById("stopSection");

let path = "../json/";

// //countdown 
// let timeLeft = 16; //비디오 로딩 시간 약 1초 + 준비시간 10초 + 운동시간 5초 = 16초
// let countDown = setInterval(function(){
//     timeLeft -=1 ;
//     if (timeLeft <= 0) {
//         clearInterval(countDown);
//         state = 'waiting';
//         console.log("운동끝!!!", state);

//         readySection.style.display = "none";
//         workoutSection.style.display = "none";
//         stopSection.style.display = "block";
//         video.pause();
//         brain.saveData('test-data');

//     } else if (0 < timeLeft && timeLeft <= 5) {
//         state = 'collecting';
//         console.log("운동시간", state);

//         readySection.style.display = "none";
//         workoutSection.style.display = "block";
//         workoutSection.innerHTML = "<h1 class='title'>OK!</h1><p class='desc'><span class='timer'>"+timeLeft+"</span>초 버티세요! </p>";

//     } else {
//         console.log("준비시간", state);

//         readySection.innerHTML = "<h1 class='title'>자세를 <br>맞춰주세요.</h1><p class='desc'><span class='timer'>"+(timeLeft-5)+"</span>초 후 자세를 취해주세요. </p>";
//     }
// },1000);

//countdown 
let timeLeft = 3; //비디오 로딩 시간 약 1초 + 준비시간 1초 + 운동시간 1초 = 3초
let countDown = setInterval(function(){
    timeLeft -=1 ;
    if (timeLeft <= 0) {
        clearInterval(countDown);
        state = 'waiting';
        console.log("운동끝!!!", state);

        readySection.style.display = "none";
        workoutSection.style.display = "none";
        stopSection.style.display = "block";
        video.pause();
        brain.saveData('test-data');

    } else if (0 < timeLeft && timeLeft <= 5) {
        state = 'collecting';
        console.log("운동시간", state);

        readySection.style.display = "none";
        workoutSection.style.display = "block";
        workoutSection.innerHTML = "<h1 class='title'>OK!</h1><p class='desc'><span class='timer'>"+timeLeft+"</span>초 버티세요! </p>";

    } else {
        console.log("준비시간", state);

        readySection.innerHTML = "<h1 class='title'>자세를 <br>맞춰주세요.</h1><p class='desc'><span class='timer'>"+(timeLeft)+"</span>초 후 자세를 취해주세요. </p>";
    }
},1000);

// function keyPressed(){
//     if (key == 't') {
//         brain.normalizeData();
//         brain.train({
//             epochs: 10
//         }, finished);
//     } else if (key == 's') {
//         brain.saveData('test-data');
//     } else {
//         targetLabel = key;
//         console.log(targetLabel);
//         setTimeout(function(){
//             console.log('collecting');
//             state = 'collecting';
//             setTimeout(function(){
//                 console.log('not collecting');
//                 state = 'waiting';
//             },2000);
//         },1000);
//     }
// }

function setup(){
    // video.hide();
    let poseNet = ml5.poseNet(video, modelReady);
    poseNet.on('pose', gotPoses);

    let options = {
        inputs: 34,
        outputs: 34, //1?
        task: 'classification',
        debug: true
    }
    brain = ml5.neuralNetwork(options);
}
// function brainLoaded(){
//     console.log('pose classification ready');
//     classifyPose();
// }
// function classifyPose(){
//     if (pose){
//         let inputs = [];
//         for (let i = 0; i < pose.keypoints.length; i++) {
//             let keypoint = pose.keypoints[i];
//             let X = keypoint.position.x;
//             let Y = keypoint.position.y;
//             inputs.push(X);
//             inputs.push(Y);
//         }
//         brain.classfiy(inputs, gotResult);
//     } else {
//         setTimeout(classifyPose, 100);
//     }   
// }
// function gotResult(error, results) { //자세 분석할 때 이용할 화면
//     if (results[0].confidence > 0.75){
//         poseLabel = results[0].label.toUpperCase();
//     }
//     classifyPose();
// }

// function dataReady(){
//     brain.normalizeData();
//     brain.train({
//         epochs: 10
//     }, finished);
// }
// function finished(){
//     console.log('model trained');
//     brain.save();
//     classifyPose();
// }
function gotPoses(poses){
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
            let outputs = inputs;
            // console.log(outputs.length);
            brain.addData(inputs, outputs);
        }
    }
}

// function gotPoses(poses){
//     // console.log(poses);
//     if (poses.length > 0) {
//         pose = poses[0].pose;
//         skeleton = poses[0].skeleton;
//         if (state == 'collecting') {
//             let inputs = [];
//             for (let i = 0; i < pose.keypoints.length; i++) {
//                 let keypoint = pose.keypoints[i];
//                 let X = keypoint.position.x;
//                 let Y = keypoint.position.y;
//                 inputs.push(X);
//                 inputs.push(Y);
//             }
//             // let target = [targetLabel];
//             let outputs = [];
//             outputs = inputs;
//             brain.addData(inputs, outputs);
//         }
//     }
// }
function modelReady(){
    console.log("model ready");
}
function draw(){
    // drawCameraIntoCanvas();
    // push();
    // console.log(video.width);
    ctx.save();
    ctx.scale(-1, 1);
    ctx.translate(-video.width, 0);
    ctx.drawImage(video, 0,0, 640, 480);
    drawKeypoints();
    drawSkeleton();
    ctx.restore();
    // pop();
}
function drawKeypoints(){
    if (pose) { 
        for (let i = 0; i < pose.keypoints.length; i ++) {
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
}
function drawSkeleton() {
    if (skeleton) {
        for (let i = 0; i < skeleton.length; i ++) {
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
}