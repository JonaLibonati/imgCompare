import os
from os.path import abspath
from inspect import getsourcefile

py_path = abspath(getsourcefile(lambda:0))
folder_path = py_path.replace('tst.py','')
loads_path = folder_path + 'loads/'

print(os.listdir(loads_path))