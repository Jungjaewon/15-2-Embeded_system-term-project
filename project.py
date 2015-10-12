

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



############## Message recieve and send image########
def fileSend(): 







#####################################################
camera = cv2.VideoCapture(0)
socket = None


if camera is None:
 print 'Camera Error\n'
 print 'Program will exit'


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