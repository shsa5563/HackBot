#!/usr/bin/python
#Author : Shekhar 
# this source is part of my Hackster.io project

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will publish test mqtt messages using the AWS IoT hub
# to test this program you have to run first its companion awsiotsub.py
# that will subscribe and show all the messages sent by this program

import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform
import json

import Adafruit_DHT
import sqlite3
import time
#sqlite connection code ------------start--------
conn = sqlite3.connect('hackbot.db')
curs = conn.cursor()
curs.execute('CREATE TABLE IF NOT EXISTS tb_humid_temp (datestamp REAL, temp REAL, humid REAL)')

connflag = False


#code excuted on connection to the aws-mqtt ----start----
def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#using paho client to get the AWS-Mqtt to publish and subscribe
awshost = "a2lbhwrrv8k74e.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "EnziCar_thing"
thingName = "EnziCar_thing"
caPath = "/home/pi/Downloads/root-CA.crt"
certPath = "/home/pi/Downloads/EnziCar_thing.cert.pem"
keyPath = "/home/pi/Downloads/EnziCar_thing.private.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()
