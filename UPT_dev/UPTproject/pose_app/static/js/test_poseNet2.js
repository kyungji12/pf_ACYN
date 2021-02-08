//This javascript is for singlePose 

let canvas = document.getElementById("canvas");
let video = document.getElementById("video");
let ctx = canvas.getContext("2d");

let pose ;
let skeleton ; 

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

//A function that gets called every time there's an update from the model
function gotPoses(poses){
    // console.log(poses);
    if (poses.length > 0) {
        pose = poses[0].pose;
        skeleton = poses[0].skeleton;
    }

}
function modelReady(){
    console.log("model ready");
    poseNet.singlePose(video);
}
// A function to draw ellipses over the detected keypoints
function drawKeypoints(){
//console.log("drawKeypoints");
    if (pose) { //이거 없으면 오류나니까 빼지말기
        //Loop through all the poses detected
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
// A function to draw the skeletons
function drawSkeleton() {
//console.log("drawSkeleton");
    if (skeleton) {
        //Loop throuth all the skeletons detected
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