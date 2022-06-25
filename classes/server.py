import random
import threading
import time
import http.server
import socketserver
import webbrowser

class simpleServer:
    def __init__(self):
        self.PORT = random.randrange(1000,9999)
        self.handler = http.server.SimpleHTTPRequestHandler
        self.URL = f'http://localhost:{self.PORT}/index.html'


    #to start simpleServer only to GET resources.
    def run(self):
        with socketserver.TCPServer(("", self.PORT), self.handler) as httpd:
            self.socket = httpd
            t1 = threading.Thread(target=self.waitAndShutdown)
            t1.start()
            print("\nserving at port", self.PORT)
            print("\nThe server will close in 5seg. You will be able to use the tool with the cache resources\n")
            try:
                httpd.serve_forever()
            except:
                self.socket.shutdown()
                print("\nClosing...")
            finally:
                t1.join()

    def waitAndShutdown (self):
        time.sleep(5)
        self.socket.shutdown()

    def openLocalHost(self):
        webbrowser.open_new_tab(self.URL)