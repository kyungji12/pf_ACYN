// console.log("ready!!");

let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let ctx = canvas.getContext("2d");

// let noseX = 0;
// let noseY = 0;

// let eyelX = 0; //왼쪽 눈 X
// let eyelY = 0; //왼쪽 눈 Y

// let poses = [];

function drawCameraIntoCanvas(){
    //CanvasDrawImage.drawImage(image: CanvasImageSource, dx: number, dy: number): void
    ctx.drawImage(video, 0, 0, 640, 480); //canvas (0,0)위치에 640*480 크기의 video 위치시키기
}

// Create a new poseNet method : 
const poseNet = ml5.poseNet(video, modelReady);
// Listen to new 'pose' events
poseNet.on('pose', gotPoses);

// function gotPoses(results){
//     poses = results;
// }
// // When the model is loaded
// function modelReady() {
//     console.log('Model Ready!');
//   }

// let video;
// let poseNet;

// let noseX = 0;
// let noseY = 0;

// let eyelX = 0; //왼쪽 눈 X
// let eyelY = 0; //왼쪽 눈 Y

// function setup(){
// 	// createCanvas(640, 480);
// 	video = createCapture(VIDEO); 
//     // ctx.drawImage(video, 0, 0, 640, 480);
//     video.hide(); 

// 	poseNet = ml5.poseNet(video, modelReady);
// 	poseNet.on('pose', gotPoses);
// };

function gotPoses(poses){ //여러명의 포즈 인식하기
	//console.log(poses);
	if (poses.length > 0) { // ⭐️코 위치가 있다면
		let nX = poses[0].pose.keypoints[0].position.x // 코 X
		let nY = poses[0].pose.keypoints[0].position.y // 코 Y
		let eX = poses[0].pose.keypoints[1].position.x // 눈 X
		let eY = poses[0].pose.keypoints[1].position.y // 눈 Y
		noseX = lerp(noseX, nX, 0.5);
		noseY = lerp(noseY, nY, 0.5);
		eyelX = lerp(eyelX, eX, 0.5);
		eyelY = lerp(eyelY, eY, 0.5);
	}
};

function modelReady(){ //준비되면 콘솔창에 띄우기
	console.log('model ready');
};

function draw(){
	image(video, 0, 0); 
	//filter(GRAY); 

	let d = dist(noseX, noseY, eyelX, eyelY);
	
	fill(255, 0, 0);
	ellipse(noseX, noseY, d);

//이 d를 구하는 이유는 빨간코의 원근감을 위해 
// 눈 코사이의 거리 비율은 변하지 않으므로 이 길이가 커지면 가까운거, 작으면 멀어진것으로 인식
};