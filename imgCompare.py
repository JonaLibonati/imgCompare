
from inspect import getsourcefile
from os.path import abspath
import os
import sys
import json
import asyncio
import random

from classes import directory
from classes import server
from classes import menu

def toJsonFile(data, path):
        with open(path, 'w') as f:
            f.write(json.dumps(data))

def checkExisting(*paths):
    for path in paths:
        if not os.path.exists(path):
            print(f'🔴 - ERROR: File or directory does not exist. "{path}"\n')
            sys.exit()

def checkAreFiles(*paths):
    for path in paths:
        if not os.path.isfile(path):
            print(f'🔴 - ERROR: Both path should be Files. "{path}"\n')
            sys.exit()

def checkAreDirs(*paths):
    for path in paths:
        if not os.path.isdir(path):
            print(f'🔴 - ERROR: Both path should be Dirs. "{path}"\n')
            sys.exit()

def askInput(text):
    path_one = input(f"\nDrag and drop or indicate path {text}:\n")
    return path_one.replace("'","")

def askInputs(text1, text2):
    path_one = askInput(text1)
    path_two = askInput(text2)
    print('')
    return [path_one, path_two]

def instanseLoadsDir():
    py_path = abspath(getsourcefile(lambda:0))
    folder_path = py_path.replace('imgCompare.py','')
    loads1_path = folder_path + 'processor/loads1/'
    loads2_path = folder_path + 'processor/loads2/'
    loads1 = directory.Directory(loads1_path)
    loads2 = directory.Directory(loads2_path)
    loads1.empty()
    loads2.empty()
    return [loads1, loads2, folder_path]

async def simpleCompare():
    print('')
    print('--------------------------------------------------')
    inputs = askInputs('IMAGE__1__', 'IMAGE__2__')
    checkExisting(inputs[0], inputs[1])
    checkAreFiles(inputs[0], inputs[1])
    returns = instanseLoadsDir()
    loads1 = returns[0]
    loads2 = returns[1]
    folder_path = returns[2]

    image_a = directory.File(inputs[0])
    image_b = directory.File(inputs[1])

    await asyncio.gather(
        loads1.addFiles(image_a),
        loads2.addFiles(image_b))

    image_a_relPath = loads1.filesList()[0].path.replace(f'{folder_path}processor/', '')
    image_b_relPath = loads2.filesList()[0].path.replace(f'{folder_path}processor/', '')

    data = {'pair' : [image_a_relPath, image_b_relPath, image_a.name]}

    toJsonFile(data, 'processor/inputs.json')

async def multipleCompare():
    print('')
    print('--------------------------------------------------')
    print('This mode takes two directories as inputs with images inside.\nThe images to be compare should have the same name because this indicates which image to compare with.')

    inputs = askInputs('DIRECTORY__1__', 'DIRECTORY__2__')
    checkExisting(inputs[0], inputs[1])
    checkAreDirs(inputs[0], inputs[1])
    returns = instanseLoadsDir()
    loads1 = returns[0]
    loads2 = returns[1]
    folder_path = returns[2]
    print('')
    print('--------------------------------------------------')
    print('Loading images\n')
    print('PLEASE WAIT. This could take a few seconds')

    dir_a = directory.Directory(inputs[0])
    dir_b = directory.Directory(inputs[1])

    await asyncio.gather(
        loads1.addFiles(*dir_a.filesList()),
        loads2.addFiles(*dir_b.filesList()))

    data = {}
    i = 0
    for file_a in loads1.filesList():
        for file_b in loads2.filesList():
            if file_a.name == file_b.name:
                path_a = file_a.path.replace(f'{folder_path}processor/', '')
                path_b = file_b.path.replace(f'{folder_path}processor/', '')
                data.update({f'Pair{i}:' : [path_a, path_b, file_a.name]})
                i = i + 1
                break

    toJsonFile(data, 'processor/inputs.json')

def emptyTxt(txtFilePath: str):
    with open(txtFilePath, 'w') as f:
        f.write('')

def startServer():
    Server = server.simpleServer(random.randrange(1000,9999), 'processor/index.html')
    Server.openWebbrowser()
    Server.setShutdownMethod(lambda: Server.waitSignalAndShutdown())
    Server.run()

def mainMenu():
    #creating options
    op1 = menu.Option('Simple compare', lambda : asyncio.run(simpleCompare()), ' <Compare two images>')
    op2 = menu.Option('Multiple compare', lambda : asyncio.run(multipleCompare()), ' <Compare multiples images>')
    op3 = menu.Option('Exit', lambda : sys.exit())

    #e.g. Numeric Menu
    menu1 = menu.NumericMenu('---- MODE MENU ----', '\nPlease choose the compare mode\n')
    menu1.addOptions(op1, op2, op3).ask()

def main ():
    print('\n==== Image compare tool ====\n')
    mainMenu()
    startServer()

#Running app
if __name__ == '__main__':
    main ()