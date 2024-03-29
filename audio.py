import os
import sys
import subprocess
from colorama import Fore, Back, Style
from analyze import *
from ffmpeg_inputs import *
from data import *
from actions import *

def audio_results(read_file):
        # Get the raw information and make it readable
        loudnorm_result = open(read_file, 'r')
        extract_audiolevels = loudnorm_result.readlines()
        for line in extract_audiolevels: 
            if line.__contains__("input_"):
                new_line = line.replace('"', '').replace(':', '=').replace(' ', '').replace('input', 'measured').strip('\t \n ,')

                search([ 'measured_i', 'measured_tp', 'measured_lra', 'measured_thresh'], new_line, audio_levels, True)

        print(f"Audio review: {Back.GREEN}{Fore.BLACK} Success {Style.RESET_ALL}\n")
        os.system(f"rm {read_file}")

        # This is just to print the results in a user friendly way
        printables = [
                ["Integrated", "measured_i"],
                ["True Peak", "measured_tp"],
                ["LRA", "measured_lra"],
                ["Threshold", "measured_thresh"],
                ]
        print_results(printables, audio_levels, from_json=False)


