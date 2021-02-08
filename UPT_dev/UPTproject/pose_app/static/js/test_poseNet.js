// This javascript is for multiPose
let canvas = document.getElementById("canvas");
let video = document.getElementById("video");
let ctx = canvas.getContext("2d");

let poses = [];

// create video
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
      video.srcObject = stream;
      video.play();
    });
    //   navigator.mediaDevices.getUserMedia({ video: false }).catch(function(err) {
    //   // 오류 처리
    //   alert("비디오 권한을 사용하지 않으면 UPT 서비스를 이용할 수 없습니다.");
    // });
  }

//그림을 그릴 수 있는 canvas안에 video 위치시키기
function drawCameraIntoCanvas(){
// draw the video element into the canvas
    ctx.drawImage(video, 0,0, 640, 480);
// We can call both functions to draw all keypoints and the skeletons
    drawKeypoints();
    drawSkeleton();

    window.requestAnimationFrame(drawCameraIntoCanvas);
}
//Loop over the drawCameraIntoCanvas function
drawCameraIntoCanvas();

//Create a new poseNet methode with a single detection 
let poseNet = ml5.poseNet(video, modelReady);
//An event listener that returns the results when a pose is detected. 
poseNet.on('pose', gotPoses);

// poseNet.on('pose', (results) => {
//     // do something with the results
//     console.log(results);
// });

//A function that gets called every time there's an update from the model
function gotPoses(results){
    //console.log(results);
    poses = results;
}
function modelReady(){
    console.log("model ready");
    // poseNet.singlePose(video);
    poseNet.multiPose(video);
}
// A function to draw ellipses over the detected keypoints
function drawKeypoints(){
//console.log("drawKeypoints");
//Loop through all the poses detected
    for (let i = 0; i < poses.length; i += 1) {
    // For each pose detected, loop through all the keypoints
        for (let j = 0; j < poses[i].pose.keypoints.length; j += 1) {
            let keypoint = poses[i].pose.keypoints[j];
            let X = keypoint.position.x;
            let Y = keypoint.position.y;
            //Only draw an ellipse is the pose probability is bigger than 0.2
        if (keypoint.score > 0.2) {
                ctx.fillStyle = 'lavender';
            //Call this method when you want to create a new path
                ctx.beginPath();
            //draw circle
                ctx.arc(X, Y, 10, 0, 2 * Math.PI);
            //outline
                ctx.fill(); 
            }
        }
    }
}
// A function to draw the skeletons
function drawSkeleton() {
//console.log("drawSkeleton");
//Loop throuth all the skeletons detected
    for (let i = 0; i < poses.length; i += 1) {
    // For every skeleton, loop through all body connections
        for (let j = 0; j < poses[i].skeleton.length; j += 1) {
            let partA = poses[i].skeleton[j][0];
            let partB = poses[i].skeleton[j][1];
            ctx.strokeStyle = 'lavender';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(partA.position.x, partA.position.y);
            ctx.lineTo(partB.position.x, partB.position.y);
            ctx.stroke();
        }
    }
}

// function draw() {
//     var canvas = document.getElementById('canvas');
//     if (canvas.getContext) {
//         var ctx = canvas.getContext('2d');

//         var rectangle = new Path2D();
//         rectangle.rect(10, 10, 50, 50);

//         var circle = new Path2D();
//         circle.moveTo(125, 35);
//         circle.arc(100, 35, 25, 0, 2 * Math.PI);

//         ctx.stroke(rectangle);
//         ctx.fill(circle);
//     }
// }