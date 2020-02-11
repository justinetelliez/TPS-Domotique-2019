import time
import pycom
import gc

from network import LoRa
from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE
from CayenneLPP import CayenneLPP


# Disable default blue LED blink
pycom.heartbeat(False)
# Pytrack GPS
time.sleep(2)
# enable garbage collector
gc.enable()
# Enable pytrack shield
py = Pysense()
print("Pysense firmware version: " + str(py.read_fw_version()))
counter = 0
# Init sensors
li = LIS2HH12(py)       ## acceleration

xref,yref,zref = li.acceleration() ## pour la sensibilité
print("xref : " + str(xref) + ", yref :" + str(yref) + ", zref :" + str(zref))

lpp = CayenneLPP()

## acc
mvt = False
handler_counter = 0

def handler_acc(event):
        global mvt
        global handler_counter
        handler_counter += 1 
        x,y,z = li.acceleration()
        print(str(handler_counter) + " -> x : " + str(x) + ", y :" + str(y) + ", z :" + str(z))

        if ( x>xref+0.01 or x<xref-0.01 or y>yref+0.01 or y<yref-0.01 or z>zref+0.01 or z<zref-0.01 ):
                print("mouvement !")
                mvt = True

li.enable_activity_interrupt(200, 100, handler_acc)

while True:
    time.sleep(0.1)
    
    if mvt:
        lpp.reset()
        x,y,z = li.acceleration()
        lpp.add_accelerometer(1, x,y,z)

        s.setblocking(True)
        s.send(bytes(lpp.get_buffer()))
        s.setblocking(False)

        print(lora.stats())
        counter = counter + 1
        print(counter)
        mvt = False

        pycom.rgbled(0x001400) ## led verte
        time.sleep(5)
        pycom.rgbled(0x000000)

    