#Author : Shekhar
#The code is for making Raspberry Pi as the Server : Web Socket Communication
#!/usr/bin/python
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import RPi.GPIO as GPIO
from time import sleep
import json

import Adafruit_DHT
import sqlite3
import datetime
import boto3
from picamera import PiCamera 
from time import sleep

#sqlite connection code ------------start--------
conn = sqlite3.connect('hackbot.db')
curs = conn.cursor()
curs.execute('CREATE TABLE IF NOT EXISTS tb_humid_temp (datestamp TEXT, temp REAL, humid REAL)')

#sqlite connection code ------------End--------

#Gpio configuration on the board -------start--------
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 16
Motor1B = 18
Motor1E = 22
 
Motor2A = 19
Motor2B = 21
Motor2E = 23
pir = 11

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
 
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT) 
GPIO.setup(10,GPIO.OUT) # for the Servo Motor
GPIO.setup(pir, GPIO.IN) # for the pir sensor

#Gpio configuration on the board -------end--------
camera = PiCamera()


#-----------------start the class for web socket receive and send------------
class WSHandler(tornado.websocket.WebSocketHandler):

  def check_origin(self, origin):
        return True

  def open(self):
    print 'user is connected.\n'

  def on_message(self, message):
    print 'received message: %s\n' %message


    #On message "Up" received the GPIO pin will triger the motors to go formward direction 
    if message == 'up':    
      print "Going forwards"
      
      GPIO.output(Motor1A,GPIO.HIGH)
      GPIO.output(Motor1B,GPIO.LOW)
      GPIO.output(Motor1E,GPIO.HIGH)
       
      GPIO.output(Motor2A,GPIO.HIGH)
      GPIO.output(Motor2B,GPIO.LOW)
      GPIO.output(Motor2E,GPIO.HIGH)

      GPIO.output(10,GPIO.HIGH)

      sleep(2)
    #On message "right" received the GPIO pin will triger the servo motor to turn right direction 
    elif message =="right":
      print "Right"

      GPIO.output(Motor2E,GPIO.LOW)
      GPIO.output(Motor1E,GPIO.LOW)
      
      frequency_hertz = 50
      pwm = GPIO.PWM(10, 50)

      pwm.start(7.5)
      sleep(.5)
      pwm.stop()

    #On message "left" received the GPIO pin will triger the servo motor to turn left direction 	
    elif message =="left":
      print "Left"
      
      GPIO.output(Motor2E,GPIO.LOW)
      GPIO.output(Motor1E,GPIO.LOW)
      frequency_hertz = 50
      pwm = GPIO.PWM(10, 50)

      pwm.start(12.5)
      sleep(.5)
      pwm.stop()

    #On message "rev" received the GPIO pin will triger the DC motors to turn in reverse direction 	

    elif message == 'rev':
      print "Now stop"
      
      GPIO.output(Motor1A,GPIO.LOW)
      GPIO.output(Motor1B,GPIO.HIGH)
      GPIO.output(Motor1E,GPIO.HIGH)
       
      GPIO.output(Motor2A,GPIO.LOW)
      GPIO.output(Motor2B,GPIO.HIGH)
      GPIO.output(Motor2E,GPIO.HIGH)


    elif message == 'stop':
      print "Now stop"
      
      GPIO.output(Motor2E,GPIO.LOW)
      GPIO.output(Motor1E,GPIO.LOW)
      GPIO.cleanup()

      GPIO.setmode(GPIO.BOARD)
       
      Motor1A = 16
      Motor1B = 18
      Motor1E = 22
       
      Motor2A = 19
      Motor2B = 21
      Motor2E = 23
      pir = 11

      GPIO.setup(Motor1A,GPIO.OUT)
      GPIO.setup(Motor1B,GPIO.OUT)
      GPIO.setup(Motor1E,GPIO.OUT)
       
      GPIO.setup(Motor2A,GPIO.OUT)
      GPIO.setup(Motor2B,GPIO.OUT)
      GPIO.setup(Motor2E,GPIO.OUT)
      GPIO.setup(10,GPIO.OUT)
      GPIO.setup(pir, GPIO.IN)
      
    #On message "GET" received the ADAFRUIT sensor information is fetched 	

    elif message =="get":
      humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
      if humidity is not None and temperature is not None:
        temp_value = '{0:0.1f}'.format(temperature)
        humidity_value = '{0:0.1f}'.format(humidity)
        Date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data ={}
        curs.execute("INSERT INTO tb_humid_temp(datestamp,temp,humid) VALUES (?,?,?)",(Date_time, temp_value , humidity_value))
        conn.commit()
        curs.execute("SELECT datestamp, temp, humid, AVG(temp),MIN(temp),MAX(temp),AVG(humid),MIN(humid),MAX(humid) FROM tb_humid_temp")
        for row in curs.fetchall():
          data['temp']= '{0:0.1f}*C'.format(row[1])
          data['humid']= '{0:0.1f}'.format(row[2])
          data['datestamp']= row[0]
          json_data = json.dumps(data)
        print json_data
        self.write_message(json_data)

    #On message "envi" received the camera is activated and takes picture only if the PIR sensor detects a motion
    elif message == 'envi':
      print "environment info"
      mine = 1
      while(mine):
          if(GPIO.input(11)): # check if there is a motion detected 
              
              path = '/home/pi/Final_Proj/image.jpg'
              camera.start_preview()
              sleep(.2)
              camera.capture(path)
              camera.stop_preview()

              #put the picture taken to the s3 bucket
              s3 = boto3.resource('s3')

              data = open(path,'rb')
              s3.Bucket('recog-enzicarz').put_object(Key='image.jpg',Body=data)

              client = boto3.client('rekognition')
              response = client.detect_labels(
                  Image= {
                      'S3Object':{
                          'Bucket': 'recog-enzicarz',
                          'Name': 'image.jpg',
                      },
                  }
              )
              json_data = json.dumps(response)
              self.write_message(response)              
              print(response)
              sleep(1)
              mine = mine -1
      
    else:
      self.write_message(message + ' OK')

  def on_close(self):
    print 'connection closed\n'

application = tornado.web.Application([(r'/ws', WSHandler),])

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
