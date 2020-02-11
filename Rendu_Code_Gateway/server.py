from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import urllib.parse
import serial
import sys
import logging
import threading
import time


app = Flask(__name__)
socketio = SocketIO(app)
ser = serial.Serial(sys.argv[1])  # open serial port

# l'handler lors de la premiere connection MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected: "+str(rc))
    socketio.emit("pysense")


# L'handler pour la reception d'un message MQTT
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    socketio.emit("pysense")

# Route standard du serveur qui renvoi la page web
@app.route('/')
def index():
    #only by sending this page first will the client be connected to the
    #socketio instance
    return render_template('index.html',ip=sys.argv[2])


# Fonction de thread tournant en boucle et lisant les caracteres reçu sur le port Serial,
# si il y a un "2" emet un message de type intrusion sur le socket lié a la
# page web
def serialObs():
    while 1 :
        s = ser.read(1)
        if s.decode("utf-8") == '2' :
            print('intrusion detectee')
            socketio.emit("intrusion")
    return 0

# Fonction de thread ecoutant en boucle sur le serveur MQTT de l'unistra et
def MQTTObs():
    client = mqtt.Client()

    #les handlers
    client.on_connect = on_connect
    client.on_message = on_message

    #connection au server
    client.username_pw_set("userdemo1", password="icube01")
    client.connect("loraserver.u-strasbg.fr", 1883, 60)
    client.subscribe("$SYS/applications/pysense/device/pysense-10/#")

    #ecouter pour toujours
    client.loop_forever()
    return 0

# Fonction s'executant lorsque la page web envoi l'ordre d'allumer la lumière
# via le websocket
@socketio.on('allumer')
def allumer_zig():
    print('allumer lampe')
    ser.write(b'1')
    return "OK"

# Fonction s'executant lorsque la page web envoi l'ordre d'eteindre la lumière
# via le websocket
@socketio.on('eteindre')
def eteindre_zig():
    print('eteindre lampe')
    ser.write(b'0')
    return "OK"



#Fonction main lancant les thread puis le serveur
if __name__ == "__main__":
    # Thread Zigduino
    x = threading.Thread(target=serialObs, args=())

    x.start()

    # Thread PySense
    y = threading.Thread(target=MQTTObs, args=())

    y.start()

    # Lancement du serveur
    socketio.run(app)
