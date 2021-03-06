#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import logging
import time


PORT_NUMBER = 80
logging.basicConfig(filename='simple_server.log',level=logging.INFO)


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        #logging.info(self.path)
        print "Request for " + self.path
        try:
            if self.reqCount % 400 == 0:
                print "Restarting server"
                server.socket.close()
                server.serve_forever()
            self.reqCount += 1
        except AttributeError:
            self.reqCount = 1


        if self.path == "/helloworld":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("Hello World")
            return

        #Open the static file requested and send it
        f = open('/data/pictures/img' + self.path.replace('/','') + '.jpg') 
        self.send_response(200)
        self.send_header('Cache-Control', 'public, max-age=31536000')
        self.send_header('ETag', '696897' + self.path.zfill(2) + '96a7c876b7e')
        self.send_header('Date', time.strftime("%a, %d %Y %H:%M:%S GMT"))
        self.send_header('Last-Modified', 'Sat, 10 Jun 2010 10:00:00 GMT')
        self.send_header('Content-type','image/jpg')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        print "Request for " + self.path + " completed!"

        return

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".mp4"):
                mimetype='video/mp4'
                sendReply = True
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True 

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + 'videos' + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return


        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()