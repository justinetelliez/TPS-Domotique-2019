import socket
import binascii
import pycom
import time
import os
import machine
from machine import UART
from network import WLAN
from network import LoRa

uart = UART(0, baudrate=115200)
os.dupterm(uart)

# wifi_ssid = 'My_SSID'
# wifi_pass = 'myPassPass'
#
# if machine.reset_cause() != machine.SOFT_RESET:
#     wlan = WLAN(mode=WLAN.STA)
#     wlan.connect(wifi_ssid, auth=(WLAN.WPA2, wifi_pass), timeout=5000)
#     while not wlan.isconnected():
#          machine.idle()

# Disable WLAN and save energy
wlan = WLAN()
wlan.deinit()

# Disable heartbeat LED
pycom.heartbeat(False)

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTAA authentication parameters
app_eui = binascii.unhexlify('1234567890123456')
app_key = binascii.unhexlify('47900f2bded548cb345c658d3175eb98')

print("DevEUI: %s" % (binascii.hexlify(lora.mac())))
print("AppEUI: %s" % (binascii.hexlify(app_eui)))
print("AppKey: %s" % (binascii.hexlify(app_key)))

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)

# wait until the module has joined the network
while not lora.has_joined():
    pycom.rgbled(0x140000)
    time.sleep(1.0)
    pycom.rgbled(0x000000)
    time.sleep(4.0)
    print('Not yet joined...')

print('OTAA joined')
pycom.rgbled(0x001400)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

machine.main('main.py')
