import os
import sys
import subprocess
from colorama import Fore, Back, Style
from analyze import *
from settings import *
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
        print_results(printables, audio_levels, has_space=False)


# This function fixes the audio. It does let us choose between stereo and dual mono. 
def audio_fix(title, integrated, true_peak, lra, threshold, dual_mono_string, code):
    fixed_output = f"{title.removesuffix('.mov')}_FIXED.mov"
    
    fix_code = code.format(source=title, integrated=integrated, true_peak=true_peak, lra=lra, threshold=threshold, dual_mono=dual_mono_string, fixed_output=fixed_output)

    fix = subprocess.Popen(fix_code, shell=True, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    for line in fix.stderr:
        sys.stdout.write(line)
    fix.wait()
