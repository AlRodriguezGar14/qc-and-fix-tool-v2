import sys
import subprocess
from colorama import Fore, Back, Style
from analyze import *
from ffmpeg_inputs import *
from data import *
from actions import *



def ffmpeg_fix(code):
    

    fix = subprocess.Popen(code, shell=True, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    for line in fix.stderr:
        sys.stdout.write(line)
    fix.wait()

    print(f'\n\n{Back.GREEN}{Fore.BLACK}Your video has been fixed{Style.RESET_ALL}\n')


