import threading
import time
import http.server
import socketserver
import webbrowser
import os

#Global Variable
close = False
dir_path = ''

class simpleServer:
    def __init__(self, PORT: int, relativeURL: str, dirPath: str) -> None:
        self.path = dirPath
        self._setDirectory()
        self.PORT = PORT
        self.handler = ServerHandler
        self.URL = f'http://localhost:{self.PORT}/{relativeURL}'

    def _setDirectory(self):
        global dir_path
        dir_path = self.path

    #to start simpleServer only to GET resources.
    def run(self) -> None:
        with socketserver.TCPServer(("", self.PORT), self.handler) as httpd:
            self.socket = httpd
            t1 = threading.Thread(target = self.shutdownMethod)
            t1.start()
            print("\nserving at port", self.PORT)
            print("\nThe server will close automatically. You will be able to use the tool with the cache resources\n")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                self.socket.shutdown()
                print("\n🔴 - KeyboardInterrupt. Closing server.")
            finally:
                t1.join()

    def setShutdownMethod(self, ShutdownMethod) -> None:
        self.shutdownMethod = ShutdownMethod

    def waitTimeAndShutdown (self, time: int) -> None:
        time.sleep(time)
        self.socket.shutdown()
        print("\n🟢 Waiting time finish. Closing server.")

    def waitSignalAndShutdown(self) -> None:
        global close
        if close != True:
            time.sleep(1)
            self.waitSignalAndShutdown()
        else:
            self.socket.shutdown()
            print("\n🟢 Load finish. Closing server.")

    def openWebbrowser(self) -> None:
        webbrowser.open_new_tab(self.URL)

class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=dir_path, **kwargs)

    def do_CLOSE(self):
        global close
        close = True
