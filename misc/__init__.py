import sys
import os
from datetime import datetime
import subprocess
import struct

def log(str, col):
    time = datetime.now().strftime('%H:%M:%S')
    log = "[Decompiler]" + ' ' + str
    print log

def CheckArch():
    ar = 8 * struct.calcsize("P")
    if ar == 32:
        arc = 32
        return arc
    elif ar == 64:
        arc = 64
        return arc
    else:
        arc = 0
        return arc
