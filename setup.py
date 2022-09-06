import sys
import os
from cx_Freeze import setup, Executable
import requests
from multiprocessing import Queue

#FILES
files = [
    ".needed\\",
    "alarmWindow.ui",
    "viewWindow.ui"
]

#TARGET
target = Executable(
    script = "alarmWindow.py",
    base = "WIN32GUI"
)

#SETUP
setup(
    name = "Alarm [REMASTERED]",
    version = "1.0",
    description = "",
    author = "Debtanu Gupta",
    options = {"build_exe" : {"include_files": files}},
    executables = [target]
)