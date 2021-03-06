#!/usr/bin/python
import cv2
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import time
import os
import signal
import subprocess
import time
import sys

capture=None
global server



# Class that sets up HTTP Server and Converts - We need not modify this
class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print self.path
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			capture = cv2.VideoCapture(rtsplink)
			while(capture.isOpened()):
				#try:
				        #capture = cv2.VideoCapture(rtsplink)
					rc,img = capture.read()
					#cv2.imshow(img)
					if (rc==True):
					        #return
					        #print("Not rc")
					        #continue
					        #while not rc:
					        #    capture.release()
						#    captureagain = cv2.VideoCapture(rtsplink)#continue#
						#    rc,img = captureagain.read()
						#    captureagain.release()
					    imgRGB = img#cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
					    imgRGB = cv2.resize(imgRGB,(960,380))
					    r, buf = cv2.imencode(".jpg",imgRGB)
					    self.wfile.write("--jpgboundary\r\n")
					    self.send_header('Content-type','image/jpeg')
					    self.send_header('Content-length',str(len(buf)))
					    self.end_headers()
					    self.wfile.write(bytearray(buf))
					    self.wfile.write('\r\n')
					    time.sleep(0.005)
					else:
					    print("rc not true")
					    continue   
				#except Exception as e:#KeyboardInterrupt:
				#	print("Exception in Capturing",e)#break
			capture.release()	 
			return
		#if self.path.endswith('.html') or self.path=="/":
		#	self.send_response(200)
		#	self.send_header('Content-type','text/html')
		#	self.end_headers()
		#	self.wfile.write('<html><head></head><body>')
		#	self.wfile.write('<img src="http://127.0.0.1:9090/cam.mjpg"/>')
		#	self.wfile.write('</body></html>')
		#	return

def main():#camname):
          global rtsplink
          global capture
	  ## While loop just in case rtsp link returns error
	  # camname is the ip address of the camera that the user selects - camname is passed on from django side
	  #print("CAM",camname)
	  camname = "64"
 	  rtsplink1 = "rtsp://admin:camera12@192.168.1."
	  rtsplink2 = ":554/Streaming/channels/1/"
	  #rtsp link that we form based on the recieved ip
	  rtsplink =  rtsplink1 + camname + rtsplink2
	  
	  print("RTSPLINK",rtsplink)
	  
	  #Existing sample rtsp link from the internet -  for testing purposes
	  #if(int(camname) in [229,213,225,227,203]):
	  #    samplelink = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
	  #else:    
	  #    samplelink = "rtsp://localhost:8554/ds-test"
	  
	  #capture = cv2.VideoCapture(rtsplink)
	  #while(capture.isOpened()):
	  #  ret,frame=capture.read()
	  #  print("Entering cap")
	  #  if(ret==True):
	  #    print("Ret true")
	  #    cv2.imshow("Frame",frame)
	  #    if(cv2.waitKey(25) & 0xFF == ord('q')):
	  #      break
	  #  else:
	  #    continue#break  
	  
	  #These lines do not matter
	  #capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640); 
	  #capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 320);
	  
	  #Killing existing HTTP servers to start a new one
	  try:
	      command = "netstat -ltnp | grep 9090"
              c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
              stdout, stderr = c.communicate()
              #Getting process id of the existing HTTP Server process
              pid = int(stdout.decode().strip().split(' ')[-1].split('/')[0])
              print(pid)
              os.kill(pid, signal.SIGTERM)
	  except Exception as e:
	      print("Killing exception",str(e))
	  #Sleep for 2 seconds is necessary for HTTP Servers to restart again    
	  time.sleep(5)    
	    
	  #Starting new HTTP Server for our stream  
	  try:
	   	server = HTTPServer(('',9090),CamHandler)
	  	print "server started"
	  	server.serve_forever()
	  except Exception as e:
	  	capture.release()
	  	server.socket.close()
	  	print("Exception in Main",e)
	  capture.release()
	  #cv2.destroyAllWindows()
          server.socket.close()	
          command = "netstat -ltnp | grep 9090"
          c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
          stdout, stderr = c.communicate()
          #Getting process id of the existing HTTP Server process
          pid = int(stdout.decode().strip().split(' ')[-1].split('/')[0])
          print(pid)
          os.kill(pid, signal.SIGTERM)
        
if __name__ == '__main__':
	main()#sys.argv[1])

