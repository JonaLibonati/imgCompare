from inspect import getsourcefile
from os.path import abspath
import os
import random
import shutil
import threading
import time
import http.server
import socketserver
import webbrowser

py_path = abspath(getsourcefile(lambda:0))
folder_path = py_path.replace('imgCompare.py','')
loads_path_imageOne = folder_path + '/loads/imageOne.jpg'
loads_path_imageTwo = folder_path + '/loads/imageTwo.jpg'
SERVERPORT = random.randrange(1000,9999)
index_url = f'http://localhost:{SERVERPORT}/index.html'

class server:
    def __init__(self, PORT):
        self.PORT = PORT
        self.handler = http.server.SimpleHTTPRequestHandler
        self.URL = f'http://localhost:{self.PORT}/index.html'

    def runServer(self):
        with socketserver.TCPServer(("", self.PORT), self.handler) as httpd:
        t1 = threading.Thread (target=down, args=(httpd, ))
        t2 = threading.Thread (target=copyImgToLoads, args=(path_image_one, loads_path_imageOne))
        t3 = threading.Thread (target=copyImgToLoads, args=(path_image_two, loads_path_imageTwo))
        t1.start()
        t2.start()
        t3.start()
        print("\nserving at port", PORT)
        print("\nThe server will close in 5seg. You will be able to use the tool with the cache resources\n")
        try:
            httpd.serve_forever()
        except:
            print("\nClosing...")
        finally:
            t1.join()
            t2.join()
            t3.join()

#to start simpleServer only to GET resources.
def runServer (port):

    PORT = port
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        t1 = threading.Thread (target=down, args=(httpd, ))
        t2 = threading.Thread (target=copyImgToLoads, args=(path_image_one, loads_path_imageOne))
        t3 = threading.Thread (target=copyImgToLoads, args=(path_image_two, loads_path_imageTwo))
        t1.start()
        t2.start()
        t3.start()
        print("\nserving at port", PORT)
        print("\nThe server will close in 5seg. You will be able to use the tool with the cache resources\n")
        try:
            httpd.serve_forever()
        except:
            print("\nClosing...")
        finally:
            t1.join()
            t2.join()
            t3.join()

def down (socket):
    time.sleep(5)
    socket.shutdown()
    socket.server_close()

def copyImgToLoads (forigen, fdestino):
    if os.path.exists(forigen):
        with open(forigen, 'rb') as forigen:
            with open(fdestino, 'wb') as fdestino:
                shutil.copyfileobj(forigen, fdestino)

def main ():
    print('**** Image compare tool ****')

    path_image_one = input("\nDrag and drop or indicate path or URL of the image one:\n")
    path_image_one = path_image_one.replace("'", '')

    path_image_two = input("\nDrag and drop or indicate path or URL of the image two:\n")
    path_image_two = path_image_two.replace("'", '')

    webbrowser.open_new_tab(index_url)

    runServer(SERVERPORT)


#Running app

if __name__ == '__main__':
    main ()