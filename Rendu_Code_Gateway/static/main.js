// Ajout des listeners sur click.

document.getElementById('stopAlarm').addEventListener("click", function(event) {
  (function(event) {
    var f = document.getElementById("intrusion").innerHTML = "Zone sécurisée";
  }).call(document.getElementById('stopAlarm'), event);
  });

var socket = io();
socket.on('connect', function() {
    console.log('socket connected to server Flask');
});


// Transmet l'ordre d'allumer ou d'eteindre la lumiere via les sockets
document.getElementById('eteindre').addEventListener("click", function(event) {
  (function(event) {
        console.log('eteindre lumiere');
        socket.emit('eteindre');
        var f = document.getElementById("lum").innerHTML = "Lumière : éteinte";


  }).call(document.getElementById('eteindre'), event);
});

document.getElementById('allumer').addEventListener("click", function(event) {
  (function(event) {
        console.log('allumer lumiere');
        socket.emit('allumer');
        var f = document.getElementById("lum").innerHTML = "Lumière : allumée";

  }).call(document.getElementById('allumer'), event);
});

// Débloque la sécurité empechant le spam de d'interruption au robot
document.getElementById('unblock').addEventListener("click", function(event) {
  (function(event) {
        console.log('deblocage');
        inInterrupt = true;
  }).call(document.getElementById('unblock'), event);
});

// Reception du message signalant l'intrusion de la part de la zigduino
socket.on('intrusion',function(){
      var f = document.getElementById("intrusion").innerHTML = "Intrusion détectée !!";
      var cmdZig = new ROSLIB.Topic({
        ros : ros,
        name : 'zigduino',
        messageType : 'std_msgs/String'
      });

      var string = new ROSLIB.Message({
        data : 'Capteur : zigduino'
      });

      if(!inInterrupt){
        console.log('envoi ordre zigduino');
        cmdZig.publish(string);
        inInterrupt = true;
      }

  });
  var nbMvt=0;

// Reception du message signalant le mouvement de la part de la PySense
socket.on('pysense',function(){
  nbMvt++;
  var f = document.getElementById("pysense").innerHTML = nbMvt;
  var cmdPy = new ROSLIB.Topic({
    ros : ros,
    name : 'pysense',
    messageType : 'std_msgs/String'
  });

  var string = new ROSLIB.Message({
    data : 'Capteur : pysense'
  });



  if(!inInterrupt){
    console.log('envoi ordre pysense');
    cmdPy.publish(string);
    inInterrupt = true;
  }
  });
