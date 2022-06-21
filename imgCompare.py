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

class imagePair:

    def __init__(self, path_image_one, path_image_two):
        py_path = abspath(getsourcefile(lambda:0))
        folder_path = py_path.replace('imgCompare.py','')
        self.loads_path = folder_path + 'loads/'
        self.path_post_one = self.loads_path + os.path.basename(path_image_one)
        self.path_post_two = self.loads_path + os.path.basename(path_image_two)
        self.path_origin_one = path_image_one
        self.path_origin_two = path_image_two
        self.list_paths = [(self.path_origin_one, self.path_post_one), (self.path_origin_two, self.path_post_two)]

    def addPairToDir(self):
        #if os.path.exists(self.path_image_one):
            #with open(self.path_image_one, 'rb') as forigen:
                #with open(self.loads_path_imageOne, 'wb') as fdestino:
                    #shutil.copyfileobj(forigen, fdestino)
        #if os.path.exists(self.path_image_two):
            #with open(self.path_image_two, 'rb') as forigen:
                #with open(self.loads_path_imageTwo, 'wb') as fdestino:
                    #shutil.copyfileobj(forigen, fdestino)
        for tuple in self.list_paths:
            if os.path.exists(tuple[0]):
                with open(tuple[0], 'rb') as forigin:
                    with open(tuple[1], 'wb') as fdestino:
                        shutil.copyfileobj(forigin, fdestino)

    def addPairToList(self, array_target):
        item_to_add = [self.path_post_one, self.path_post_two]
        array_target.append(item_to_add)

    def emptyPairDir(self):
        if os.path.exists(self.loads_path):
            for image in os.listdir(self.loads_path):
                os.remove(self.loads_path + image)

    #def addPairs ()

def listToJson (list, jsonFile):
    with open(jsonFile, 'w') as f:
        f.write(f'"{list}"')

def main ():
    print('**** Image compare tool ****')

    path_image_one = input("\nDrag and drop or indicate path or URL of the image one:\n")
    path_image_one = path_image_one.replace("'", '')

    path_image_two = input("\nDrag and drop or indicate path or URL of the image two:\n")
    path_image_two = path_image_two.replace("'", '')

    json_list = []

    image_pair = imagePair(path_image_one, path_image_two)
    image_pair.emptyPairDir()
    image_pair.addPairToDir()
    image_pair.addPairToList(json_list)

    listToJson(json_list, 'inputs.json')

    #simple_server = simpleServer()
    #simple_server.openLocalHost()
    #simple_server.run()

#Running app
if __name__ == '__main__':
    main ()