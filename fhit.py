#!/usr/bin/env python3

import time
from colorama import Fore, Style
from analyze import *
from meta import *
from black_frames import *
from settings import *
from audio import *
from actions import *
from remove_dp_frames import remove_dp_frames
import argparse


parser = argparse.ArgumentParser(description='app for the AppleHIT program')

parser.add_argument("title")
parser.add_argument('--full', '-f', help='Use it if you want a full review', action='store_true')
parser.add_argument('--metadata', '-m', help='Get the video metadata', action='store_true')
parser.add_argument('--black_frame', '-bf', help='Search for black frames', action='store_true')
parser.add_argument('--audio', '-a', help='Analyze the audio', action='store_true')
parser.add_argument('--role', '-r', help='Decide if the video is main or preview. Default value is main', choices=['main', 'm', 'preview', 'p'], default='main')
parser.add_argument('--channels', '-ch', help='Decide if the audio is stereo or dual mono. Default value is stereo', choices=['stereo', 's', 'dual_mono', 'dual mono', 'dm'], default='stereo')
parser.add_argument('--duplicate_frames', '-dp', help='Remove duplicate frames from the video. Default value is 5', choices=['5', '6', '25'])



args = parser.parse_args()

title = args.title.replace(' ', '')
full_review = args.full
metadata = args.metadata
black_frame = args.black_frame
audio = args.audio
channels = args.channels
if channels == 'stereo' or channels == 's':
    channels = 'stereo'
else:
    channels = 'dual mono'

role = args.role
if role == 'main' or role == 'm':
    role = 'main'
else:
    role = 'preview'

duplicate_frames = args.duplicate_frames

metadata_note, black_frame_note, audio_note, full_note, duplicate_frames_note = "", "", "", "", ""


if metadata == False and black_frame == False and audio == False and duplicate_frames == None:
    full_review = True
    
if full_review == True:
    metadata = True
    black_frame = True
    audio = True


if duplicate_frames != None: duplicate_frames_note = print_todos('Remove duplicate frames', duplicate_frames)
if metadata == True: metadata_note = print_todos('Analyze metadata', metadata)
if black_frame == True: black_frame_note = print_todos('Search for black frames', black_frame)
if audio == True: audio_note = print_todos('Analyze the audio levels', audio)

print(f"\n\t{Fore.CYAN}The video role is:{Style.RESET_ALL} {role}\n\t{Fore.CYAN}The audio is:{Style.RESET_ALL} {channels}\n\t{Fore.CYAN}The location is:{Style.RESET_ALL} {title}")
print(f'\n\tI will work on...{metadata_note}{black_frame_note}{audio_note}{duplicate_frames_note}\n')


validate_input = False
while validate_input == False:
    validate_input = input_validator('Is this information ok? Yes[y] / No[n]', 'yes', 'y', 'no', 'n')
    if validate_input == False:
        print('We will have to review all the information again. Or you can write the commands again if you script the script with ^C')
        title = input("Drag your file here: ").replace(' ', '')
        role = input_validator("Is your title main[m] or preview[p]?", "main", "m", "preview", "p")
        if role == 'main' or role == 'm':
            role = 'main'
        else:
            role = 'preview'
        channels = input_validator("Is your title stereo[s] or dual mono[dm]?", "stereo", "s", "dual mono", "dm")
        if channels == 'stereo' or channels == 's':
            channels = 'stereo'
        else:
            channels = 'dual mono'
        print(f"\n\t{Fore.CYAN}The video role is:{Style.RESET_ALL} {role}\n\t{Fore.CYAN}The audio is:{Style.RESET_ALL} {channels}\n\t{Fore.CYAN}The location is:{Style.RESET_ALL} {title}")

time.sleep(0.5)

if metadata:
    # metadata analysis
    analysis(datacheck, title, 7, temp_output)
    video_data['timecode_track'] = metadata_results(temp_output)
    if video_data['timecode_fix']:
        ffmpeg_audio_fix = remove_timecode_and_fix_audio
    input('Press Enter to continue...')

if black_frame:
    #black_frames_check
    black_frame_check(role, title)
    input('Press Enter to continue...')



if audio:
    # audio analysis
    analysis(audiocheck, title, 2, temp_output)
    audio_results(temp_output)
    
    want_fix_audio = input_validator("Do you want to fix the audio? y/n", "yes", "y", "no", "n")
    if want_fix_audio:
        time.sleep(0.2)
        # Fix the audio. The code varies depending if the video is stereo or dual mono
        if channels == "stereo":
            audio_fix(title, audio_levels['measured_i'], audio_levels['measured_tp'], audio_levels['measured_lra'], audio_levels['measured_thresh'], "dual_mono=false", ffmpeg_audio_fix)
        elif channels == "dual mono":
            audio_fix(title, audio_levels['measured_i'], audio_levels['measured_tp'], audio_levels['measured_lra'], audio_levels['measured_thresh'], "dual_mono=true", ffmpeg_audio_fix)
        video_data['timecode_track'] = False
        video_data['timecode_fix'] = False
    else:
        print("Ok, I won't fix the audio\n")
        time.sleep(0.2)

    if video_data['timecode_fix']:
        print("Removing the timecode track...")
        time.sleep(0.5)
        timecode_remover(title, only_remove_timecode_track)
        video_data['timecode_track'] = False
        video_data['timecode_fix'] = False



if duplicate_frames != None:
    remove_dp_frames(title, duplicate_frames)

if video_data['timecode_track']:
    print("Removing the timecode track...")
    time.sleep(0.5)
    timecode_remover(title, only_remove_timecode_track)
    video_data['timecode_track'] = False
    video_data['timecode_fix'] = False


print('\nEnd of the review\n')
