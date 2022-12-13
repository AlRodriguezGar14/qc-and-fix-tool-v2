import subprocess
import os
import random
import sys
import time
from colorama import Fore, Back, Style
from settings import *
from analyze import *
from actions import *

def black_frame_check(role, title):
    print(title)
    temp_bf_top = f"package_creation_bf_top{n_output}.txt"
    temp_bf_end = f"package_creation_bf_end{n_output}.txt"

    # The code to check the black frames. It is different depending if it's main or preview and if it's top or bottom    
    formulas_top = {'preview': f'ffmpeg -hide_banner -t 6 -i {title} -vf blackframe=amount=100:thresh=17 -f null -',
                'main': f'ffmpeg -hide_banner -t 1 -i {title} -vf blackframe=amount=100:thresh=17 -f null -'}

    formulas_bottom = {'preview': f'ffmpeg -hide_banner -sseof -5 -i {title} -vf blackframe=amount=100:thresh=17 -f null -',
                    'main': f'ffmpeg -hide_banner -sseof -1 -i {title} -vf blackframe=amount=100:thresh=17 -f null -'}


    with open(temp_bf_top, 'w') as f : 
        bf_top = subprocess.Popen(formulas_top[role], shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        for line in bf_top.stderr:
            sys.stdout.write(line)
            f.write(line)
        bf_top.wait()
    with open(temp_bf_end, 'w') as f : 
        bf_end = subprocess.Popen(formulas_bottom[role], shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        for line in bf_end.stderr:
            sys.stdout.write(line)
            f.write(line)
        bf_end.wait()

    # We get the info from the subprocess and make it readable line by line
    extract_bf_top = open(temp_bf_top, 'r').readlines()
    extract_bf_end = open(temp_bf_end, 'r').readlines()
    top_results= []
    end_results = []

    top_black_frames = False
    for line in extract_bf_top:
        
        if line.__contains__("frame:0"):
            top_black_frames = True
            # We only check how many black frames there are if the very first one is black. If not, it's an auto-fail
        if top_black_frames == True:    
            if line.__contains__("black:100"):
                # We already know what we need to know. 
                # We change all the lines with a black frame for something that we can count (Success word in this case).
                # 1 'Success' means 1 black frame. We only have to count the length of the array.
                new_line = line.replace(line, 'Success')
                top_results.append(new_line)

    if len(top_results) > 0:
        print(f'{Fore.BLACK}{Back.GREEN}\n I found at least {len(top_results)} black frame(s) at the top {Style.RESET_ALL}')
    else:
        print(f"{Fore.BLACK}{Back.RED}\nThe title does't start with a black frame{Style.RESET_ALL}")

    for line in extract_bf_end:
        if line.__contains__("black:100"):
            new_line = line.replace(line, 'Success')
            end_results.append(new_line)

    if len(end_results) > 0:
        print(f'{Fore.BLACK}{Back.GREEN}\n I found at least {len(end_results)} black frame(s) at the end {Style.RESET_ALL}\n')
    else:
        print(f'{Fore.BLACK}{Back.RED}\nNo black frames at the end have been found{Style.RESET_ALL}\n')

    # Remove the unnecessary files (you can read the info on the terminal thanks to subprocess.Popen instead of subprocess.run)
    os.system(f"rm {temp_bf_top}")
    os.system(f"rm {temp_bf_end}")


