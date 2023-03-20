import subprocess
import os
import sys
import re
from colorama import Fore, Back, Style
from ffmpeg_inputs import *
from data import *
from analyze import *
from actions import *

def black_frame_check(role, title):
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
        formatted_line = line
        if "Parsed_blackframe_0" in line:
            parsed_bf_prefix = re.findall(r'\[(.*?)\]', line)
            formatted_line = re.sub(r'\[(.*?)\]', f'{Fore.GREEN}[{parsed_bf_prefix[0]}]{Style.RESET_ALL}', line).replace('\n', '')
        
        if line.__contains__("frame:0 pblack:100"):
            top_black_frames = True
            # We only check how many black frames there are if the very first one is black. If not, it's an auto-fail

        if top_black_frames == True:    
            if line.__contains__("black:100"):
                # We already know what we need to know. 
                # We change all the lines with a black frame for something that we can count (Success word in this case).
                # 1 'Success' means 1 black frame. We only have to count the length of the array.
                new_line = line.replace(line, 'Success')
                top_results.append(new_line)
                print(formatted_line)
        


    for line in extract_bf_end:
        if line.__contains__("black:100"):
            parsed_bf_prefix = re.findall(r'\[(.*?)\]', line)
            formatted_line = re.sub(r'\[(.*?)\]', f'{Fore.BLUE}[{parsed_bf_prefix[0]}]{Style.RESET_ALL}', line)
            print(formatted_line)
            new_line = line.replace(line, 'Success')
            end_results.append(new_line)

    if len(top_results) > 0:
        print(f'{Fore.BLACK}{Back.GREEN}\n I found at least {len(top_results)} black frame(s) at the top {Style.RESET_ALL}\n')
    else:
        print(f"{Fore.BLACK}{Back.RED}\nThe title does't start with a black frame{Style.RESET_ALL}")

    if len(end_results) > 0:
        print(f'{Fore.BLACK}{Back.GREEN}\n I found at least {len(end_results)} black frame(s) at the end {Style.RESET_ALL}\n')
        bottom_black_frames = True
    else:
        print(f'{Fore.BLACK}{Back.RED}\nNo black frames at the end have been found{Style.RESET_ALL}\n')
        bottom_black_frames = False

    # Remove the unnecessary files (you can read the info on the terminal thanks to subprocess.Popen instead of subprocess.run)
    os.system(f"rm {temp_bf_top}")
    os.system(f"rm {temp_bf_end}")

    if top_black_frames == False or bottom_black_frames == False:
        add_bf_or_not = input_validator("Do you want to add black frames? y/n", "yes", "y", "no", "n")
        return add_bf_or_not
    else:
        return False





def fadeout_position(input):
    try:
        duration = float(video_data['duration_copy'].removeprefix('duration ='))
    except:
        print('Let me get the information needed for this fix')
        analysis(datacheck, input)
        metadata_results(temp_output)
        duration = float(video_data['duration_copy'].removeprefix('duration ='))

    if video_data['r_frame_rate'] != 'r_frame_rate = 0/0':
        framerate = float(video_data['r_frame_rate'].removeprefix('r_frame_rate ='))
    else:
        framerate = float(video_data['r_frame_rate_copy'].removeprefix('r_frame_rate ='))

    total_frames = framerate * duration

    print(f'total frames of the title: {total_frames}')
    # 0.3 is around 9-7 frames and the duration of the fadeout is around 6 and 4 frames6 and 4 frames6 and 4 frames6 and 4 frames6 and 4 frames
    start_of_fadeout_audio = duration - 0.3
    
    # The video fadeout starts 5 frames before the end and the transition lasts 2 frames (we have 2-3 black frames as output)
    start_of_fadeout_video = total_frames - 5

    print(f'The fadeout starts at {start_of_fadeout_video}')

    return(start_of_fadeout_video, start_of_fadeout_audio)


