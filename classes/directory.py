import os
import shutil

class Directory:

    def __init__(self, loads_path):
        self.path = loads_path
        self.fileSets = []
        self.files = []

    def empty(self):
        if os.path.exists(self.path):
            for file in os.listdir(self.path):
                os.remove(self.path + file)

    def addSet(self, *args):
        self.fileSets.append(args)

    def addFiles(self, *args):
        for arg in args:
            self.files.append(arg)

    def copyFiles(self):
        for i, file in enumerate(self.files) :
            if os.path.exists(file.path):
                with open(file.path, 'rb') as forigin:
                    file.path = f'{self.path}{file.name}__{i}'
                    with open(file.path, 'wb') as fdestino:
                        shutil.copyfileobj(forigin, fdestino)

    def filesToJson(self):
        json = {}
        for i , file in enumerate(self.files):
            json.update({f'file{i}' : file.path})
        return json

    def setsToJson(self):
        json = {}
        for i , list in enumerate(self.fileSets):
            set_list = []
            for file in list:
                set_list.append(file.path)
            json.update({f'set{i}' : set_list})
        return json

    class File:
        def __init__(self, path):
            self.path = path
            self.name = os.path.basename(self.path)