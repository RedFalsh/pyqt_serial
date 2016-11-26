from distutils.core import setup

import py2exe

import sys

 

#this allows to run it with a simple double click.

sys.argv.append('py2exe')

 

py2exe_options = {

        "includes": ["sip"],

        "dll_excludes": ["MSVCP90.dll",],

        "compressed": 1,

        "optimize": 2,

        "ascii": 0,

        "bundle_files": 1,

        }

 

setup(

      name = 'sample',

      version = '1.0',

      windows = ['main.py',],

      data_files=[("",

                   [r"C:\Python33\Lib\site-packages\PyQt5\libEGL.dll"]),

                  ("platforms",

                   [r"C:\Python33\Lib\site-packages\PyQt5\plugins\platforms\qwindows.dll"])],

      zipfile = None,

      options = {'py2exe': py2exe_options}

      )