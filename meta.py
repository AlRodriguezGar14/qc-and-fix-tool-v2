import os
import sys
import subprocess
import json
from colorama import Fore, Back, Style
from analyze import *
from actions import *
from ffmpeg_inputs import *
from data import *


def extract_duration(duration):
    extract_duration = round(float(duration), 3)
    seconds = extract_duration % (24*3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60


    if int(hour) < 1:
        duration_format = f'{int(minutes)} minute(s) and {int(seconds)} seconds'
    else:
        duration_format = f'{int(hour)} hour(s), {int(minutes)} minute(s) and {int(seconds)} seconds'

    return duration_format


def metadata_results(read_file):
    with open(read_file, 'r') as f:
        extract_data = f.read()

    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    print("===========\n")
    data = json.loads(extract_data)
    

    values_to_search = [ 'codec_name', 'codec_type', 'codec_tag_string', 'width', 'height', 'sample_aspect_ratio', 'field_order', 'r_frame_rate', 'color_space', 'color_primaries', 'color_transfer', 'duration']

    for stream in data["streams"]:
        if stream["codec_type"] == "video":
            for value in values_to_search:
                video_data[value] = stream.get(value, "Info Missing")

        if stream["codec_type"] == "data":
            video_data["timecode_track"] = True



    video_data["duration"] = extract_duration(video_data["duration"])
    
    printables = []
    for key, value in video_data.items():
        
        printables.append([key, value])
    
    print(printables)

    return
# def old_metadata_results(read_file):
#     
#     data_results = open(read_file, 'r')
#     extract_data = data_results.readlines()
#     
#     timecode_track_status = f"\n{Back.GREEN}{Fore.BLACK} No timecode track found {Style.RESET_ALL}\n"
#
#     # burn the information in video_data. It's very importat to know the given outpout in order to make this work. Writting the original ffprobe code in order to get only the streams list is not working correctly.
#     for line in extract_data:
#         new_line = line.strip(' , \t \n').replace('":', ' =').replace('"', '')
#         
#         # color_range removed. ffprobe is not catching it (unknown error)
#         search([ 'codec_name', 'codec_type', 'codec_tag_string', 'width', 'height', 'sample_aspect_ratio', 'field_order', 'r_frame_rate', 'color_space', 'color_primaries', 'color_transfer', 'duration'], new_line, video_data)
#
#         if video_data['timecode_track']:
#             timecode_track_status = f"\n{Back.RED}{Fore.BLACK} Timecode track found. {Style.RESET_ALL}\n"
#             break
#
#     print(timecode_track_status)
#
#
#     ## Give format to the duration. Also, move the duration from duration_copy to duration (the original is duration_ts that complicates too much giving it a format)
#     try:
#         extract_duration = round(eval(video_data['duration_copy'].removeprefix('duration =')), 3)
#         seconds = extract_duration % (24*3600)
#         hour = seconds // 3600
#         seconds %= 3600
#         minutes = seconds // 60
#         seconds %= 60
#         
#
#
#         if int(hour) < 1:
#             duration_format = f'{int(minutes)} minute(s) and {int(seconds)} seconds'
#         else:
#             duration_format = f'{int(hour)} hour(s), {int(minutes)} minute(s) and {int(seconds)} seconds'
#
#         video_data['duration'] = f"duration = {duration_format}"
#
#     except:
#         video_data['duration'] = video_data['duration_copy']
#
#     
#     if video_data['codec_type'] == "codec_type = audio":
#
#         # Remove the temporary file. If we reach here there has not been errors. That means that it is not necessary.    
#         os.system(f"rm {read_file}")
#
#         ## When fixing a video with compressor, the audio channel goes before the video channel. That's why I use the values with _copy at the end. 
#         ## When they come later I just save them as copy in order to avoid duplications and have more control (The data can be added in any random way depending the output)
#         printables = [
#         ["Codec Type", "codec_type_copy"],
#         ["Codec Name", "codec_name_copy"],
#         ["Width", "width"],
#         ["Height", "height"],
#         ["Codec Tag String", "codec_tag_string_copy"],
#         ["Aspect Ratio", "sample_aspect_ratio"],
#         ["Field Order", "field_order"],
#         ["Frame Rate (in fps)", "r_frame_rate_copy"],
#         ["Color Space", "color_space"],
#         ["Color Primaries", "color_primaries"], 
#         ["Color Transfer", "color_transfer"],
#         # ["Color Range", "color_range"],
#         ["Duration", "duration"],
#         ]
#
#
#
#
#         try:
# # Convert the framerate to the software standard   
#             video_data['r_frame_rate_clean'] = round(eval(video_data['r_frame_rate_copy'].removeprefix('r_frame_rate = ')), 3)
#             int_of_float = int(video_data['r_frame_rate_clean'])
#             if (int_of_float == 30) or (int_of_float == 24) or (int_of_float == 25):
#                 video_data['r_frame_rate_copy'] = f"r_frame_rate = {int_of_float}"
#             else:
#                 rounded = round(float(video_data['r_frame_rate_clean']), 3)
#
#                 video_data['r_frame_rate_copy'] = f"r_frame_rate = {rounded}"
#         except:
#             print("\nNo data available.\n")
#             
#
#
#
#         print_results(printables, video_data, has_space=True)  
#             
#
#
#     elif video_data['codec_type'] == "codec_type = video":
#         try:
#             # Convert the framerate to the software standard   
#             video_data['r_frame_rate_clean'] = round(eval(video_data['r_frame_rate'].removeprefix('r_frame_rate = ')), 3)
#             int_of_float = int(video_data['r_frame_rate_clean'])
#             if (int_of_float == 30) or (int_of_float == 24) or (int_of_float == 25):
#                 video_data['r_frame_rate'] = f"r_frame_rate = {int_of_float}"
#             else:
#                 rounded = round(float(video_data['r_frame_rate_clean']), 3)
#
#                 video_data['r_frame_rate'] = f"r_frame_rate = {rounded}"
#                 
#         except: 
#             print("\nNo data available.\n")
#
#         # Remove the temporary file. If we reach here there has not been errors. That means that it is not necessary.    
#         os.system(f"rm {read_file}")
#         
#         printables = [
#                 ["Codec Type", "codec_type"],
#                 ["Codec Name", "codec_name"],
#                 ["Width", "width"],
#                 ["Height", "height"],
#                 ["Codec Tag String", "codec_tag_string"],
#                 ["Aspect Ratio", "sample_aspect_ratio"],
#                 ["Field Order", "field_order"],
#                 ["Frame Rate (in fps)", "r_frame_rate"],
#                 ["Color Space", "color_space"],
#                 ["Color Primaries", "color_primaries"], 
#                 ["Color Transfer", "color_transfer"],
#                 # ["Color Range", "color_range"],
#                 ["Duration", "duration"],
#                 ]
#
#         
#         print_results(printables, video_data, has_space=True)
#
#     if video_data['timecode_track']:
#         video_data['timecode_fix'] = input_validator("Do you want to remove the timecode track? y/n", "yes", "y", "no", "n")
#         if video_data['timecode_fix'] == True:
#             print('\nThe timecode track will be removed\n')
#             return True
#             # global ffmpeg_audio_fix
#             # ffmpeg_audio_fix = remove_timecode_and_fix_audio
#         else:
#             print("\nThe timecode track won't be removed\n")
#             return False
#
#
#
#
#
#
#
#
