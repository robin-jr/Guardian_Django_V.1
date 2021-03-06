#!/usr/bin/python
'''
	orig author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server
'''
import cv2
from http.server import BaseHTTPRequestHandler,HTTPServer
import time

capture=None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print (self.path)
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					rc,img = capture.read()
					if not rc:
						continue
					imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
					r, buf = cv2.imencode(".jpg",imgRGB)
					#self.wfile.write("--jpgboundary\r\n")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(len(buf)))
					self.end_headers()
					self.wfile.write(bytearray(buf))
					self.wfile.write('\r\n'.encode())
					time.sleep(0.1)
				except KeyboardInterrupt:
					break
			return
		#if self.path.endswith('.html') or self.path=="/":
		#	self.send_response(200)
		#	self.send_header('Content-type','text/html')
		#	self.end_headers()
		#	self.wfile.write('<html><head></head><body>')
		#	self.wfile.write('<img src="http://127.0.0.1:9090/cam.mjpg"/>')
		#	self.wfile.write('</body></html>')
		#	return

def actualConvert():#(camnum):
	global capture
	print("Reached actualConvert")
	capture = cv2.VideoCapture("rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov")#("/home/gilfoyle/Downloads/VID-20191129-WA0004.mp4")
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640); 
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 320);
	try:
		server = HTTPServer(('',9090),CamHandler)
		print ("server started")
		server.serve_forever()
	except Exception as e:
	        print("EXCEPTION",str(e))	
	#except KeyboardInterrupt:
	#	capture.release()
	#	print ("server ended")
 	#	server.socket.close()

if __name__ == '__main__':
	actualConvert()
