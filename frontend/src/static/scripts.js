var socket = io();

//list of speedometer elements from the html
const speedoList = [
  document.getElementById('speedo1'), document.getElementById('speedo2'), document.getElementById('speedo3'),
  document.getElementById('speedo4'), document.getElementById('speedo5'), document.getElementById('speedo6'),
  document.getElementById('speedo7'), document.getElementById('speedo8')
];
//list of camera stream elements from the html
const streams = [
  document.getElementById('stream1'), document.getElementById('stream2'), document.getElementById('stream3')
];

const taskInfo = [
  document.getElementById("task-1.1-info"), document.getElementById("task-1.2-info"), document.getElementById("task-1.3-info"),
  document.getElementById("task-2.1-info"), document.getElementById("task-2.2-info"), document.getElementById("task-3.1-info")
];

const rightContainer = document.getElementsByClassName('right-container');


//function to decide if the shaded area in the speedometer should be red or green based on the angle
function colorToAngle(angle){
  if(angle < 0){
    return `rgb(200, 0, 0)`
  }else if(angle > 0){
    return `rgb(0, 200, 0)`
  }else{
    return `rgb(0, 0, 0)`
  }
}

//uses canvas to draw a speedometer based on a given thruster velocity
function drawSpeedo(velo, canvas){
  //convert thruster velocity to angle
  const angle = velo * (90/127)

  //set canavs to 2d and then clear it
  const speedo = canvas.getContext('2d');
  speedo.clearRect(0, 0, canvas.width, canvas.height);

  //define canvas line characteristics
  speedo.lineWidth = 2;
  speedo.strokeStyle = 'white';

  //define canvas arc characteristics
  const arcColor = colorToAngle(angle);
  speedo.fillStyle = arcColor;

  //set centers and radius
  const centerX = canvas.width / 2;
  const centerY = canvas.height;
  const radius = 100;

  let startAngle = 0;
  let endAngle = 0;

  //determine start and end angle by the sign of the angle
  if(angle >= 0){
    startAngle = 3 * Math.PI / 2; 
    endAngle = startAngle + (angle * Math.PI / 180);
  }else if(angle < 0){
    endAngle = 3 * Math.PI / 2; 
    startAngle = endAngle + (angle * Math.PI / 180);
  }

  //draw the shaded
  speedo.beginPath();
  speedo.arc(centerX, centerY, radius, startAngle, endAngle);
  speedo.lineTo(centerX, centerY);
  speedo.fill();

  //draw the lines
  speedo.beginPath();
  speedo.arc(centerX, centerY, radius, Math.PI, 2 * Math.PI);
  speedo.stroke();


}

//generated a random number between -127 and 127
function genRand(){
  return Math.random() * 258 - 127;
}

function hideTasks(){
  for(var i = 0; i < 6; i++){
    taskInfo[i].classList.add("hidden")
  }
}

function showTasks(i){
  hideTasks();
  document.getElementById("task-2-and-3").classList.add("hidden");
  document.getElementById("task-1").classList.add("hidden");
  taskInfo[i].classList.remove("hidden");
  rightContainer[0].style.gridTemplateRows = '60% 10% 10% 10% 10%';
}

//generated speedometers with random velocities
for(var i = 0; i < 8; i++){
  drawSpeedo(genRand(), speedoList[i]);
}

document.getElementById('inertial-data').addEventListener("click", function() {
  hideTasks();
  document.getElementById("task-2-and-3").classList.remove("hidden");
  document.getElementById("task-1").classList.remove("hidden");
  rightContainer[0].style.gridTemplateRows = '30% 30% 10% 10% 10% 10%';
});

/* implementation to switch the camera streams
var temp = streams[0].src;
streams[0].src = streams[1].src;
streams[1].src = temp;
streams[0].load;
streams[1].load;
*/

document.getElementById('task-1.1').addEventListener("click", function() {
  showTasks(0);
});

document.getElementById('task-1.2').addEventListener("click", function() {
  showTasks(1);

});

document.getElementById('task-1.3').addEventListener("click", function() {
  showTasks(2);


});

document.getElementById('task-2.1').addEventListener("click", function() {
  showTasks(3);
});

document.getElementById('task-2.2').addEventListener("click", function() {
  showTasks(4);
});

document.getElementById('task-3.1').addEventListener("click", function() {
  showTasks(5);
});
socket.on('depth', function(msg) {
  msg = JSON.parse(msg);
  document.getElementById("depth-data").innerHTML = "Depth : " + msg.data.toFixed(2);
});

socket.on('pi_temp', function(msg) {
  msg = JSON.parse(msg);
  document.getElementById("temp-data").innerHTML = "Temperature: <br>" + msg.data.toFixed(2) + "&deg C";
});

socket.on('leak_sensor', function(msg){
  msg = JSON.parse(msg);

  var leak = Boolean(msg.Bool);

  if(leak){
    document.body.style.backgroundColor = "red";
  }
  
});

socket.on('surface_imu', function(msg){
  msg = JSON.parse(msg);

  document.getElementById("accel-data").innerHTML = "Acceleration : &lt" + msg.accel[0].toFixed(2) + ", " + msg.accel[1].toFixed(2) + ", " + msg.accel[2].toFixed(2) + "&gt m/s";

  document.getElementById("pry-data").innerHTML = "Gyro : &lt" + msg.gyro[0].toFixed(2) + ", " + msg.gyro[1].toFixed(2) + ", " + msg.gyro[2].toFixed(2) + "&gt &deg";
});


document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".photo-button").forEach(button => {
    button.addEventListener("click", async (e) => {
      e.stopPropagation();

      const camera = button.dataset.camera;
      const original = button.textContent;

      button.textContent = "⏳";
      button.disabled = true;

      try {
        const res = await fetch(`/api/photo/${camera}`, {
          method: "POST"
        });

        const data = await res.json();

        if (data.status === "ok") {
          button.textContent = "✅";
          setTimeout(() => button.textContent = original, 1000);
        } else {
          throw new Error("Photo failed");
        }
      } catch (err) {
        console.error(err);
        button.textContent = "❌";
        setTimeout(() => button.textContent = original, 1500);
      } finally {
        button.disabled = false;
      }
    });
  });
});
