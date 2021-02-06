// console.log('ml5 version : ', ml5.version);
let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
//캔버스는 처음에 비어있습니다. 무언가를 표시하기 위해서, 어떤 스크립트가 랜더링 컨텍스트에 접근하여 그리도록 할 필요가 있습니다
//<canvas> 요소는 getContext() 메서드를 이용해서, 랜더링 컨텍스트와 (렌더링 컨텍스트의) 그리기 함수들을 사용할 수 있습니다.  
let ctx = canvas.getContext("2d");

// let poseNet;
// let pose = [];
let pose ;

// let skeleton;

function drawCameraIntoCanvas(){
    ctx.drawImage(video, 0, 0, 640, 480);

}

const poseNet = ml5.poseNet(video, modelReady);
poseNet.on('pose', gotPoses);

function modelReady(){
    console.log("model ready!");
}


// // setup();
// function setup(){
//     // console.log("Voilá ! Canvas ! ");
//     createCanvas(640, 480);

//     video = createCapture(VIDEO);
//     video.hide();

//     poseNet = ml5.poseNet(video, modelLoaded);
//     poseNet.on('pose', gotPoses);
// }
// function gotPoses(poses){
//     // console.log(poses); //17개의 신체 위치 좌표가 표시된다. 
//     if (poses.length > 0) {
//         pose = poses[0].pose;
//         skeleton = poses[0].skeleton;
//     }
// }
// function modelLoaded(){
//     console.log('poseNet ready!');
// }

// function draw(){
//     image(video, 0,0);
// }

// let video;
// let poseNet;

// let noseX = 0;
// let noseY = 0;

// function setup(){
// 	createCanvas(640, 480);
// 	video = createCapture(VIDEO); 
//     video.hide(); 

// 	poseNet = ml5.poseNet(video, modelReady);
// 	poseNet.on('pose', gotPoses);
// };

function gotPoses(poses){ //여러명의 포즈 인식하기
	//console.log(poses);
	if (poses.length > 0) { // ⭐️코 위치가 있다면
        pose = poses[0].pose;
		noseX = poses[0].pose.keypoints[0].position.x //콘솔을 살펴보면 나온다
		noseY = poses[0].pose.keypoints[0].position.y
	}
};

// function modelReady(){ //준비되면 콘솔창에 띄우기
// 	console.log('model ready');
// };

function draw(){
	// image(video, 0, 0); 
	// //filter(GRAY); 
	
	fill(255, 0, 0);
	ellipse(noseX, noseY, 50); // 코 위치한 부분에 fill 
};