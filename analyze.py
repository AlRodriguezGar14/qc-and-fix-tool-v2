import subprocess
import sys
import time
from colorama import Back, Style
from audio import *
from ffmpeg_inputs import *
from data import *
from meta import *
from actions import *





def want_to_analyze(target, function, title):
    func = {"audio_checker": analysis, 
            "meta_checker": analysis}
    params = {"audio_checker": [audiocheck, title, 2, temp_output], 
            "meta_checker":[datacheck, title, 7, temp_output]}

    while True:
        question = input_validator(f"Do you want to analyze the {target}? y/n", "yes", "y", "no", "n")
        time.sleep(0.2)
        if question:
            func[function](*params[function])
            if target == "audio":
                audio_results(temp_output)
                return True

            if target == "video metadata":
                metadata_results(temp_output)
                global video_meta_analyzed
                video_meta_analyzed = True
                return True

            else:
                break
            break

        else:
            return False





# For security won't use Shell=True until the next function when everything is ok
# Analysis of the audio levels.
def analysis(what_do, input, source_index, temp_output):
    with open(temp_output, 'w') as f:

        print('\nTime to do some research. I will have all the information in a moment.\nThis can take some minutes, so don not worry. You will have your report ⏳\n')
        
        # I don't want to launch to Shell=True in order to avoid malware (if they introduce something that is not a title, the script will crash). That's why I have to find where in the array is the title. It makes the code uglier and slower to write/scalate/fix, but it's safer.
        what_do['command'][source_index] = input
        
        # Thanks to using Popen, I display the subprocess in the screeen while it is being written at temp_output
        scan = subprocess.Popen(what_do['command'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        # Some commands save the information at stderr and some others at stdout. The only way to know this is testing the code. (this code block can be improved in the future)
        if what_do['output'] == 'stderr':
            for line in scan.stderr:
                sys.stdout.write(line)
                f.write(line)
            scan.wait()
        elif what_do['output'] == 'stdout':
            for line in scan.stdout:
                sys.stderr.write(line)
                f.write(line)
            scan.wait()
        else:
            print(f"{Back.RED}Error{Style.RESET_ALL}, the output information is missing, the information won't be saved.")

        if scan.returncode != 0:
            print(f"{Back.RED}Error{Style.RESET_ALL}")

 

       



