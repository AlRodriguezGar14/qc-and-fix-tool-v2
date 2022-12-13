import subprocess
import sys
import time
from settings import remove_duplicate_frames as ffmpeg_dp


def remove_dp_frames(title, cycle):

    output = f"{title.removesuffix('.mov')}_DP-FRAMES_REMOVED.mov"

    remove_dpf = ffmpeg_dp.format(source=title, cycle_int=cycle, fixed_output=output)
    
    fix = subprocess.Popen(remove_dpf, shell=True, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    for line in fix.stderr:
        sys.stdout.write(line)

    fix.wait()


