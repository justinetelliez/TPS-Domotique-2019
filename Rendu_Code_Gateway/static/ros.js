

ros.on('connection', function() {
  console.log('Connected to ROS websocket server.');
});

ros.on('error', function(error) {
  console.log('Error connecting to ROS websocket server: ', error);
});

ros.on('close', function() {
  console.log('Connection to ROS websocket server closed.');
});

// Bouton d'interruption manuelle zigduino du robot
document.getElementById('zigInt').addEventListener("click", function(event) {
  (function(event) {
    var cmdZig = new ROSLIB.Topic({
      ros : ros,
      name : 'zigduino',
      messageType : 'std_msgs/String'
    });

    var string = new ROSLIB.Message({
      data : 'Bouton : zigduino'
    });



    if(!inInterrupt){
      console.log('envoi ordre zigduino');
      cmdZig.publish(string);
      inInterrupt = true;
    }

  }).call(document.getElementById('zigInt'), event);
  });

// Bouton d'interruption manuelle pysense du robot
document.getElementById('pyInt').addEventListener("click", function(event) {
  (function(event) {
    var cmdPy = new ROSLIB.Topic({
      ros : ros,
      name : 'pysense',
      messageType : 'std_msgs/String'
    });

    var string = new ROSLIB.Message({
      data : 'Bouton : pysense'
    });



    if(!inInterrupt){
      console.log('envoi ordre pysense');
      cmdPy.publish(string);
      inInterrupt = true;
    }

  }).call(document.getElementById('pyInt'), event);
  });

// Subscriber ecoutant la fin d'un goal du robot
var listener = new ROSLIB.Topic({
  ros : ros,
  name : 'arrive',
  messageType : 'std_msgs/String'
});

var nbTraj = 0;

listener.subscribe(function(message) {
  console.log('Received message on ' + listener.name + ': ' + message.data);
  nbTraj++;
  var f = document.getElementById("nbTrajRobot").innerHTML = nbTraj;

  inInterrupt = false;
});
