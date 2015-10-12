

import argparse
import datetime
import imutils
import time
import cv2
import cv 


camera = cv2.VideoCapture(0)


if camera is None:
 print 'Camera Error\n'
 print 'Program will exit'
 


while( camera.isOpened() ):
 val, frame = camera.read()
 cv2.imshow("Image", frame)

 key = cv2.waitKey(30)

 