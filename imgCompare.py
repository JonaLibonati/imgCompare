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
import json

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

class loads:

    def __init__(self, loads_path):
        self.path = loads_path
        self.imagePairs = []

    def empty(self):
        if os.path.exists(self.path):
            for image in os.listdir(self.path):
                os.remove(self.path + image)

    def addPair(self, Pair):
        self.imagePairs.append(Pair)

    def copyPair(self):
            #if os.path.exists(self.path_image_one):
                #with open(self.path_image_one, 'rb') as forigen:
                    #with open(self.loads_path_imageOne, 'wb') as fdestino:
                        #shutil.copyfileobj(forigen, fdestino)
            #if os.path.exists(self.path_image_two):
                #with open(self.path_image_two, 'rb') as forigen:
                    #with open(self.loads_path_imageTwo, 'wb') as fdestino:
                        #shutil.copyfileobj(forigen, fdestino)
            for pair in self.imagePairs :
                for i, image in enumerate(pair.images) :
                    if os.path.exists(image.path):
                        with open(image.path, 'rb') as forigin:
                            image.path = f'{self.path}{image.name}__{i}'
                            with open(image.path, 'wb') as fdestino:
                                shutil.copyfileobj(forigin, fdestino)

    def toJson(self):
        json = {}
        for i , pair in enumerate(self.imagePairs):
            pair_list = []
            for image in pair.images:
                pair_list.append(image.path)
            json.update({f'pair{i}' : pair_list})
            print(json)
        return json

    class imagePair:
        def __init__(self, image_a, image_b):
            #self.path_post_one = path + os.path.basename(path_image_one)
            #self.path_post_two = path + os.path.basename(path_image_two)
            self.image_a = image_a
            self.image_b = image_b
            self.images = [self.image_a, self.image_b]

    class image:
        def __init__(self, path):
            self.path = path
            self.name = os.path.basename(self.path)

def toJsonFile(data, path):
        with open(path, 'w') as f:
            f.write(json.dumps(data))

def main ():
    print('**** Image compare tool ****\n')

    path_image_one = input("Drag and drop or indicate path or URL __1__:\n")
    path_image_one = path_image_one.replace("'","")
    path_image_two = input("Drag and drop or indicate path or URL __2__:\n")
    path_image_two = path_image_two.replace("'","")

    py_path = abspath(getsourcefile(lambda:0))
    folder_path = py_path.replace('imgCompare.py','')
    loads_path = folder_path + 'loads/'

    loadsDir = loads(loads_path)
    loadsDir.empty()

    image_a = loadsDir.image(path_image_one)
    image_b = loadsDir.image(path_image_two)
    imagePair = loadsDir.imagePair(image_a, image_b)

    loadsDir.addPair(imagePair)
    loadsDir.copyPair()

    toJsonFile(loadsDir.toJson(), 'inputs.json')

    #simple_server = simpleServer()
    #simple_server.openLocalHost()
    #simple_server.run()

#Running app
if __name__ == '__main__':
    main ()