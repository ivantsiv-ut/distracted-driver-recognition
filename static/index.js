const video = document.querySelector('#video');
const canvas = document.querySelector('#canvas');
const startButton = document.querySelector('#start');
//const ping = new Audio('static/ping-82822.mp3');
const beep = new Audio('static/beep-6-96243.mp3');


startButton.onclick = () => {
  if ('mediaDevices' in navigator && navigator.mediaDevices.getUserMedia) {
    startStream();
    sendToServer();
  }
};

const startStream = async () => {
  const constraints = {
    audio: false,
    video: {
      width: {
        max: 640,
      },
      height: {
        max: 480,
      }
    }
  };
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  video.srcObject = stream;
  video.play();
};

const sendToServer = () => {
  canvas.getContext('2d').drawImage(video, 0, 0);
  //ping.play();

  const httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = () => {
    if (httpRequest.readyState == XMLHttpRequest.DONE) {
        console.log(httpRequest.responseText);
        if (httpRequest.responseText == 'talking') {
            beep.play();
        }
    }
  }
  httpRequest.open('POST', '/screenshot');
  httpRequest.setRequestHeader("Content-Type", "application/json");
  httpRequest.send(JSON.stringify({"image": canvas.toDataURL('image/png')}));

  setTimeout(sendToServer, 3000);
};