from analyze import *
from meta import *
from black_frames import *
from settings import *
from audio import *
from actions import *
from remove_dp_frames import remove_dp_frames
from add_black_frames import *
from ffmpeg_fixer import *
import argparse

output = '/Users/albertorodriguez/Desktop/FIXED.mov'

def fadeout_position(input):
    try:
        duration = float(video_data['duration_copy'].removeprefix('duration ='))
    except:
        print('Let me get the information needed for this fix')
        analysis(datacheck, input, 7, temp_output)
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

    




