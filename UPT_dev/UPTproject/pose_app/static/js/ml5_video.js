//This javascript is for singlePose 

let canvas = document.getElementById("canvas");
let video = document.getElementById("video");
let ctx = canvas.getContext("2d");
let pose ;
let skeleton ; 

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
      video.srcObject = stream;
      video.play();
    });
  }
function drawCameraIntoCanvas(){
    ctx.drawImage(video, 0,0, 640, 400);
    drawKeypoints();
    drawSkeleton();
    window.requestAnimationFrame(drawCameraIntoCanvas);
}
drawCameraIntoCanvas();

let poseNet = ml5.poseNet(video, modelReady);
poseNet.on('pose', gotPoses);

function gotPoses(poses){
    if (poses.length > 0) {
        pose = poses[0].pose;
        skeleton = poses[0].skeleton;
    }
}
function modelReady(){
    console.log("model ready");
    poseNet.singlePose(video);
}
function drawKeypoints(){
    if (pose) { //이거 없으면 오류나니까 빼지말기
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