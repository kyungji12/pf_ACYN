//This javascript is for singlePose 
let canvas = document.getElementById("canvas");
let video = document.getElementById("video");
let ctx = canvas.getContext("2d");

let pose ;
let skeleton ; 

let state = 'waiting';
let pose_arr = [];

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
      video.srcObject = stream;
      video.play();
    });
}

let readySection = document.getElementById("readySection");
let workoutSection = document.getElementById("workoutSection");
let stopSection = document.getElementById("stopSection");


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

        $('#stopBtn').click(function(){
            sendJson();
        });

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

function setup(){
    // video.hide();
    let poseNet = ml5.poseNet(video, modelReady);
    poseNet.on('pose', gotPoses);
}
function gotPoses(poses){
    if (poses.length > 0) {
        pose = poses[0].pose;
        skeleton = poses[0].skeleton;
        if (state == 'collecting') {
            // console.log(pose);
            let results = [];
            for (let i = 0; i < pose.keypoints.length; i++) {
                let keypoint = pose.keypoints[i];
                let X = keypoint.position.x;
                let Y = keypoint.position.y;
                let score = keypoint.score ;
                if (score < 0.5 ) {
                    results.push("NaN");
                    results.push("NaN");
                    // console.log("NaN",keypoint.part,i,score, X);
                    // console.log("NaN",keypoint.part,i,score, Y);
                } else {
                    results.push(X);
                    results.push(Y);
                    // console.log(keypoint.part,i,score, X);
                    // console.log(keypoint.part,i,score, Y);
                }
                // pose_arr.push(results);
            }
            // console.log(results);
            pose_arr.pop(results);
            pose_arr.push(results);
            console.log(pose_arr);
        }
        // console.log(pose_arr);
    }
}
function sendJson(){
    $.ajax({
        type: "POST",
        url: "/result/",
        dataType: "json",
        data: JSON.stringify(pose_arr),
        contentType: "application/json;charset=UTF-8",
        success: function (data, response) {
          console.log("response");
          console.log(data);
        //   $(".title").text("");
        //   $(".desc").text("");
        //   $(".desc").text(data);
        },
        error: function (jqXHR, status, error) {
          console.log(status, error);
        },
    });
}
function modelReady(){
    console.log("model ready");
}
function draw(){
    ctx.save();
    ctx.scale(-1, 1);
    ctx.translate(-video.width, 0);
    ctx.drawImage(video, 0,0, 640, 480);
    drawKeypoints();
    drawSkeleton();
    ctx.restore();
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
            ctx.stroke();
        }
    }
}