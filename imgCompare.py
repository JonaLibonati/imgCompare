
from inspect import getsourcefile
from os.path import abspath
import json

from classes.directory import *
from classes.server import *
from classes.menu import *

def toJsonFile(data, path):
        with open(path, 'w') as f:
            f.write(json.dumps(data))

def simpleCompare():
    path_image_one = input("Drag and drop or indicate path or URL __1__:\n")
    path_image_one = path_image_one.replace("'","")
    path_image_two = input("Drag and drop or indicate path or URL __2__:\n")
    path_image_two = path_image_two.replace("'","")

    py_path = abspath(getsourcefile(lambda:0))
    folder_path = py_path.replace('imgCompare.py','')
    loads_path = folder_path + 'loads/'

    loads = Directory(loads_path)
    loads.empty()

    image_a = loads.File(path_image_one)
    image_b = loads.File(path_image_two)

    loads.addFiles(image_a, image_b)
    loads.addSet(image_a, image_b)

    loads.copyFiles()

    toJsonFile(loads.setsToJson(), 'inputs.json')
    toJsonFile(loads.filesToJson(), 'inputs.json')

    simple_server = simpleServer()
    simple_server.openLocalHost()
    simple_server.run()

def multipleCompare():
    pass

def main ():
    print('**** Image compare tool ****\n')

    #creating options
    option1 = Menu.Option('Simple compare', lambda : simpleCompare(), ' <Compare two images>')
    option2 = Menu.Option('Multiple compare', lambda : multipleCompare(), ' <Compare multiples images>')

    #e.g. Numeric Menu
    menu1 = NumericMenu('Mode Menu', '  Please choose the compare mode\n')
    menu1.addOptions(option1, option2).ask()

#Running app
if __name__ == '__main__':
    main ()