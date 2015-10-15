

import argparse
import datetime
import imutils
import time
import cv2
import cv 
import socket
from socket import *
import os
import thread
import Rpi.GPIO as GPIO


Motor = 0
Birght = 0
Msg = ''
file_path = 'image.jpg'
delay = ''
send_mail = ''
num_of_picture = ''
back_setting = ''
On_setting == ''
############## Message recieve and send image########
# msg fotmat delay/send_mail/num_of_picture/back_setting/On_setting
def fileSend():
 while True:
  msg = socktet.recv()
  tuple = msg.split('/')

  delay = tuple[0]
  send_mail = tuple[1]
  num_of_picture = tuple[2]
  back_setting = tuple[3]
  On_setting = tuple[4]

  if On_setting == "0": # Send mail
    print On_setting
    for i in int( num_of_picture ):
     


  elif On_setting == "1": # Send file to app
    print On_setting
    for i in int( num_of_picture ):
     cv2.imwrite(file_path, frame2)
     f = open( file_path , 'r')
     l = f.read()
     while(l):
      socket.send(l)
      l = f.read()
     f.close()





#####################################################
camera = cv2.VideoCapture(0)
socket = None


if camera is None:
 print 'Camera Error\n'
 print 'Program will exit'
 os_exit(0)


##################################################
################### GPIO Setting## ###############
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, False)
GPIO.setup(24, False)

##################################################

 


##################################################
################### Socket Setting ###############

socket = socket(AF_INET , SOCK_STREAM)
socket = setsockopt(SOL_SOCKET , SO_REUSEADDR , 1)

port = 7500


socket.listen(('' , port))
socket.listen(5)

client , addr = socket.accept()

##################################################

################### Image process  ###############

while( camera.isOpened() ):
 val, frame = camera.read()
 cv2.imshow("Image", frame)

 key = cv2.waitKey(30)

 if key == ord('q'):
      break

##################################################

socket.close
camera.release()
cv2.destroyAllWindows()