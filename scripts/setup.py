from cx_Freeze import setup, Executable
import sys
import os

base = None

if sys.platform == 'win32':
    base = "Win32GUI"
    # base = "Console"


executables = [Executable("app.py", base=base)]

options = {
    'build_exe': {
        'includes': ["os"],
        'include_files': [r"C:\Users\imman\AppData\Local\Programs\Python\Python38-32\DLLs\tcl86t.dll",
                          r"C:\Users\imman\AppData\Local\Programs\Python\Python38-32\DLLs\tk86t.dll"],
        'excludes': ["numpy.random._examples"]
    },

}

setup(
    name="London Coin",
    version="1.0",
    description="Build python app",
    options=options,
    executables=executables
)