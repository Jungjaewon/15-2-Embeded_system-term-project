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
import random
import sys
import signal
import smtplib
import numpy
#from email.MTMEImage import MIMEImage
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

Motor = 90
Bright = 0.5
Msg = ''
file_path = 'image.jpg'
delay = ''
send_mail = ''
num_of_picture = ''
back_setting = ''
On_setting = ''
f_num = 0;
camera = ''
frame = ''
check = 0 # false
text = ''

###################Signal Handler   #####################
def sinal_handler(signal , frame):
	print "Interrupt!!!!"
	GPIO.cleanup()
	sys.exit(0)
#########################################################


################### GPIO Setting## ###############
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

GPIO.output(15, GPIO.LOW) # RED
GPIO.output(14, GPIO.LOW) # GREEN
pwm = GPIO.PWM(18, 50)
#pwm.start(7.5)
##################################################

################### Socket Setting ###############
signal.signal(signal.SIGINT , sinal_handler)
socket = socket(AF_INET , SOCK_STREAM)
socket.setsockopt(SOL_SOCKET , SO_REUSEADDR , 1)

port = 7500


socket.bind(('' , port))
socket.listen(5)

##################################################

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
 global send_mail
 global camera
 global check
 global text
 global pwm
 sound_file = ""
 string = ""
 GPIO.output(14, GPIO.HIGH) # GREEN
 client , addr = socket.accept()
 print "accept"
 GPIO.output(14, GPIO.LOW) # GREEN
 GPIO.output(15, GPIO.HIGH) # RED
 while True:
  msg = client.recv(1024)
  tuple = msg.split('/')
  print tuple
  delay = tuple[0]

  if msg == '':
   print "User Log out"
   pwm.stop()
   GPIO.output(15, GPIO.LOW) # RED
   thread.start_new_thread(fileSend,())
   return
  if len(tuple) != 1:
   send_mail = tuple[1]
   num_of_picture = tuple[2]
   back_setting = tuple[3]
   On_setting = tuple[4]
 
  if delay == 'm+':
    Motor = Motor + 5
    duty = float(Motor) / 10.0 + 2.5
    pwm.start(2.5)
    #pwm.ChangeDutyCycle(2.5)
    time.sleep(2)
    #pwm.stop()
    print Motor
  elif delay == 'm0':
    Motor = 90
    duty = float(Motor) / 10.0 + 2.5
    pwm.start(7.5)
    #pwm.ChangeDutyCycle(7.5)
    time.sleep(2)
    #pwm.stop()
    print Motor
  elif delay == 'm-':
    Motor = Motor - 5
    duty = float(Motor) / 10.0 + 2.5
    pwm.start(12.5)
    #pwm.ChangeDutyCycle(12.5)
    time.sleep(2)
    #pwm.stop()
    print Motor

  elif delay == 'b+':
    Bright = Bright + 0.1
    camera.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, Bright)
    print Bright
  elif delay == 'b0':
    Bright = 0.5
    camera.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, Bright)
    print Bright
  elif delay == 'b-':
    Bright = Bright - 0.1
    camera.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, Bright)
    print Bright

  elif 'BG' in delay and len(delay) == 3:
    back_setting = int(delay[2])
    print back_setting

  elif On_setting == "1": # Send file to app
    print On_setting
    num = "".join( num_of_picture )
    numi = range(0 , int( num ) )
    for i in numi :
     for i in range( 0 , int(delay)):
      text = str( int(delay) - i)
      check = 1 # true
      time.sleep(1)
      check = 0 # false
     time.sleep(1)
     sound_file = str(random.randrange(1,6)) + ".mp3"
     string = "mplayer -vo x11 /home/pi/embeded/" + sound_file
     os.system(string)
     cv2.imwrite(file_path, frame)
     f = open( file_path , 'r')
     l = f.read()
     while(l):
      client.send(l)
      l = f.read()
     f.close()

  elif On_setting == "0": # Send mail 
    print On_setting
    num = "".join( num_of_picture )
    numi = range(1 , int( num ) )
    for i in range( 0 , int(delay)):
     text = str( int(delay) - i)
     check = 1 # true
     time.sleep(1)
     check = 0 # false
    time.sleep(1)
    sound_file = str(random.randrange(1,6)) + ".mp3"
    string = "mplayer -vo x11 /home/pi/embeded/" + sound_file
    os.system(string)
    cv2.imwrite(file_path, frame)
    f = open( file_path , 'r')
    l = f.read()
    while(l):
     client.send(l)
     l = f.read()
    f.close()
    MailSend()
    for i in numi :
     for i in range( 0 , int(delay)):
      text = str( int(delay) - i)
      check = 1 # true
      time.sleep(1)
      check = 0 # false
     time.sleep(1)
     sound_file = str(random.randrange(1,6)) + ".mp3"
     string = "mplayer -vo x11 /home/pi/embeded/" + sound_file
     os.system(string)
     cv2.imwrite(file_path, frame)
     MailSend() 	
     

#####################################################

############### Mail Send Function ##################

def MailSend():
	global send_mail
	global file_path
	msg = MIMEMultipart()
	msg['Subject'] = 'PhotoBox'
 	
	me = 'woodcook48@gmail.com'
	family = send_mail
	msg['From'] = me
	msg['To'] = send_mail
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
	#s.ehlo()
	#s.starttls()
	#s.ehlo()
	s.login("woodcook48","df125qwer!")
	s.sendmail(me, [send_mail], msg.as_string())
	s.quit()

###############################################################

################## Count function #######################

def Count( count ):
 global text
 cnt = range( 0 , count)
 for i in cnt:
  text = str(i)
  check = 1 # true
  time.sleep(1)
  check = 0 # false
#########################################################

################### Image process  ###############

camera = cv2.VideoCapture(0)

if camera is None:
 print 'Camera Error\n'
 print 'Program will exit'
 os.exit(0)

thread.start_new_thread(fileSend,())
while( camera.isOpened() ):
 val, frame = camera.read()

 #tmp = camera.get( cv2.cv.CV_CAP_PROP_BRIGHTNESS )
 #print "Bright : " + str(tmp)
 #bframe = cv2.blur(frame, (10,10))
 #frame = cv2.flip(frame,0)
 #frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
 #hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
 #lower_skin = numpy.array([0,59,0])
 #upper_skin = numpy.array([128,175,255])

 #mask = cv2.inRange(hsv , lower_skin, upper_skin)
 
 #res = cv2.bitwise_and(frame , frame, mask= mask)
 #face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 #eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

 #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

 #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
 #for (x,y,w,h) in faces:
 # cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
 # roi_gray  = gray[y:y+h, x:x+w]
 # roi_color = frame[y:y+h, x:x+w]
 # eyes = eye_cascade.detectMultiScale(roi_gray)
 # for (ex,ey,ew,eh) in eyes:
 #  cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

 if check == 1:
  cv2.putText(frame, text, (210, 320), cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 0, 255), 4)
 #cv2.imshow("mask", mask)
 #cv2.imshow("Res", res)
 cv2.imshow("Image", frame)
 key = cv2.waitKey(30)

 if key == ord('q'):
      GPIO.cleanup()
      break

##################################################

socket.close
camera.release()
cv2.destroyAllWindows()