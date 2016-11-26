# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = 'Console'
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        "include_files":['image'],
        'includes': 'atexit',
        'excludes': ['gtk',  'Tkinter'],
        "path": sys.path,
    }
}

executables = [
    Executable('main.py', base=base,icon = "main.ico")
]

setup(name='my_PyQt5',
      version='0.1',
      description='Sample cx_Freeze PyQt5 script',
      options=options,
      executables=executables
      )
