#!/usr/bin/python
#Author: Shekhar 
# this source is part of my Hackster.io project 

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will subscribe and show all the messages sent by its companion
# awsiotpub.py using the AWS IoT hub

import paho.mqtt.client as paho
import os
import socket
import ssl
import time
import json
global dict_tr
dict_tr ={}
global counter
counter =0

import sqlite3

#sqlite connection code ------------start--------
conn = sqlite3.connect('hackbot.db')
curs = conn.cursor()
curs.execute('CREATE TABLE IF NOT EXISTS tb_humid_temp (datestamp TEXT, temp REAL, humid REAL)')
#sqlite connection code ------------end--------

#Code executed after the connection to the aws-mqtt
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#" , 1 )

def on_message(client, userdata, msg):
    Date_time = time.time()
    Date_time =Date_time *1000
    Date_time = int(Date_time)
    mydict={}
    global counter
    counter = counter +1
    print counter
    mydict= eval(msg.payload)
    print (str(Date_time - int(mydict["datestamp"]))+" micro seconds")
    global dict_tr
    dict_tr[str(mydict["datestamp"])] = int(Date_time - int(mydict["datestamp"]))
    if counter == 29:
        list = []
        print sum(dict_tr.values())/len(dict_tr.values())

#using paho client to get the AWS-Mqtt to publish and subscribe
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

awshost = "a2lbhwrrv8k74e.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "EnziCar_thing"
thingName = "EnziCar_thing"
caPath = "/home/pi/Downloads/root-CA.crt"
certPath = "/home/pi/Downloads/EnziCar_thing.cert.pem"
keyPath = "/home/pi/Downloads/EnziCar_thing.private.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_forever()
