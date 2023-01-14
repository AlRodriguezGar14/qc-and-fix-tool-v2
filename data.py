import random


n_output = random.randint(99999999, 99999999999)
temp_output = f"package_creation_audiolevels{n_output}.txt"


# The dictionary where the clean information goes
# Its information is updated at audio results function
audio_levels = {
        'name':'audio levels',
        'measured_i' : "",
        'measured_tp' : "",
        'measured_lra' : "",
        'measured_thresh' : "",
        'dual_mono' : "",
        }
audio_analyzed = False
video_meta_analyzed = False
# This file is where I move all the information that ffmpeg prints to the console
# later it's going to be deleted, that's why I use a random generated number (not to remove anything useful)



# The dictionary with the metadata info
global video_data
video_data = {'name':'video metadata', 'timecode_track':False, 'timecode_fix':False, 'black_frames_fix':False,}




