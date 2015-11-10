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
import RPi.GPIO as GPIO

import smtplib
#from email.MTMEImage import MIMEImage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

################### GPIO Setting## ###############
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, False)
GPIO.setup(24, False)
##################################################

Motor = 0
Bright = 0
Msg = ''
file_path = 'image.jpg'
delay = ''
send_mail = ''
num_of_picture = ''
back_setting = ''
On_setting = ''
f_num = 0;
#smtp = smtplib.SMTP(HOST)


############## Message recieve and send image########
# msg fotmat delay/send_mail/num_of_picture/back_setting/On_setting
# Or b+ b0 b- m+ m0 m- BG0 BG1 BG2 BG3 BG4 
def fileSend():
 global client
 global frame
 global Bright
 global Motor
 global num_of_picture
 global back_setting
 global On_setting
 while True:
  msg = client.recv(1024)
  tuple = msg.split('/')
  print tuple
  delay = tuple[0]

  if len(tuple) != 1:
   send_mail = tuple[1]
   num_of_picture = tuple[2]
   back_setting = tuple[3]
   On_setting = tuple[4]
  
  if delay == 'm+':
    Motor = Motor + 1
    print Motor
  elif delay == 'm0':
    Motor = 0
    print Motor
  elif delay == 'm-':
    Motor = Motor - 1
    print Motor

  elif delay == 'b+':
    Bright = Bright + 1
    print Bright
  elif delay == 'b0':
    Bright = 0
    print Bright
  elif delay == 'b-':
    Bright = Bright - 1
    print Bright

  elif 'BG' in delay and len(delay) == 3:
    back_setting = int(delay[2])
    print back_setting

  elif On_setting == "0": # Send mail
    print On_setting
    num = "".join( num_of_picture )
    numi = range(0 , int( num ) )
    for i in numi :
     time.sleep(2)
     cv2.imwrite(file_path, frame)
     f = open( file_path , 'r')
     l = f.read()
     while(l):
      client.send(l)
      l = f.read()
     f.close()

  elif On_setting == "1": # Send file to app
    print On_setting
    num = "".join( num_of_picture )
    numi = range(0 , int( num ) )
    for i in numi :
     time.sleep(2)
     cv2.imwrite(file_path, frame)
     f = open( file_path , 'r')
     l = f.read()
     while(l):
      client.send(l)
      l = f.read()
     f.close()
     MailSend()

#####################################################

############### Mail Send Function ##################

def MailSend():
	global send_mail
	global file_path
	msg = MIMEMultipart()
	msg['Subject'] = 'PhotoBox'
 	
	me = 'woodcook486@naver.com'
	
	family = send_mail
	msg['From'] = me
	msg['To'] = family 
	msg.preamble = 'PhotoBox mail'
 

	fp = open(file_path, 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)
 
	# local server
	#s = smtplib.SMTP('localhost')
	#s.sendmail(me, family, msg.as_string())
	#s.quit()
 
	# another server
	s = smtplib.SMTP_SSL('smtp.gmail.com',465)
	s.login("woodcook486","df125qwer!")
	s.sendmail(me, you, msg.as_string())
	s.quit()

###############################################################


################### Socket Setting ###############

socket = socket(AF_INET , SOCK_STREAM)
socket.setsockopt(SOL_SOCKET , SO_REUSEADDR , 1)

port = 7500


socket.bind(('' , port))
socket.listen(5)

client , addr = socket.accept()
print "accpet"
##################################################

################### Image process  ###############

camera = cv2.VideoCapture(0)

if camera is None:
 print 'Camera Error\n'
 print 'Program will exit'
 os.exit(0)

thread.start_new_thread(fileSend,())
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