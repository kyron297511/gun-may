import sys
from cx_Freeze import setup, Executable

base = None
if (sys.platform == "win32"):
    base = "Win32GUI"

build_exe_options = {"include_files" : ["assets", "assets"]}

setup(name = "name of program",
      version = "0.1",
      description = "",
      options = { "build_exe" : build_exe_options },
      executables = [Executable("game.py", base = base, icon="assets/icon/icon.png")])