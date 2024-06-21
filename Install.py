import shutil
import os
import subprocess
import sys

if sys.version_info<(3,6,0):
    print("You need python 3.6 or later to run this script\n")
    exit(1)

#Confirm if virtual env is desired
print('\n-------------------------------------------------------------')
print('A virtual envrionment is recommended.')
print('The remainder of this script may overwirte existing packages.')
print('If you are sure you wish to continue press ENTER.')
print('Otherwise exit by pressing Ctrl+Z')
print('-------------------------------------------------------------')
input()

#check pip3
pip3Results = os.system("sudo apt install python3-pip")
print('pip3 Installed')

#check wheel
wheelResults = os.system("pip3 install wheel --trusted-host files.pythonhosted.org --trusted-host pypi.org")
print('wheel Installed')

#check tkinter
tkinterResults = os.system("sudo apt install python3-tk")
print('tkinter Installed')

#check binwalk
binwalkResults = os.system("sudo apt install binwalk")
print('binwalk Installed')

#check sklearn version
cythonResults = os.system("pip3 install Cython --trusted-host files.pythonhosted.org --trusted-host pypi.org")
scikitResults = os.system("pip3 install scikit-learn==0.22.1 --trusted-host files.pythonhosted.org --trusted-host pypi.org")
print('scikit and Cython Installed')

#check numpy
numpyResults = os.system("pip3 install numpy==1.22.3 --trusted-host files.pythonhosted.org --trusted-host pypi.org")
print('numpy Installed')

#check pandas
pandasResults = os.system("pip3 install pandas --trusted-host files.pythonhosted.org --trusted-host pypi.org")
print('pandas Installed')

#check matplotlib
matplotlibResults = os.system("pip3 install matplotlib --trusted-host files.pythonhosted.org --trusted-host pypi.org")
print('matplotlib Installed')

print()
print('WiiBin should be ready to run with the command: python3 WiiBin.py')
