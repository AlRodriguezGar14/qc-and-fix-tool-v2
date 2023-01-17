#!/usr/bin/env python3

import time
from colorama import Fore, Back, Style
from data import temp_output, audio_levels
from analyze import analysis
from meta import metadata_results
from black_frames import black_frame_check, fadeout_position
from ffmpeg_inputs import *
from audio import audio_results
from actions import input_validator, print_todos, what_to_fix
from ffmpeg_fixer import ffmpeg_fix
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
fixed_output = f"{title.removesuffix('.mov')}_FIXED.mov"

full_review = args.full
metadata = args.metadata
black_frame = args.black_frame
audio = args.audio
channels = args.channels
if channels == 'stereo' or channels == 's':
    channels = 'stereo'
    dual_mono = 'dual_mono=false'
else:
    channels = 'dual mono'
    dual_mono = 'dual_mono=true'

role = args.role
if role == 'main' or role == 'm':
    role = 'main'
else:
    role = 'preview'

remove_dup_frames = False
duplicate_frames = args.duplicate_frames
if duplicate_frames != None:
    remove_dup_frames = True
remove_dp_output = f"{title.removesuffix('.mov')}_REMOVED_Every_{duplicate_frames}_frames.mov"

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


remove_timecode_track, add_black_frames, fix_audio_levels = False, False, False
fadeout_start_video = 0.0
fadeout_start_audio = 0.0



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
    analysis(datacheck, title)
    remove_timecode_track = metadata_results(temp_output)
    if remove_timecode_track:
        print(f'\nRemove additional timecode: {Back.GREEN}{Fore.BLACK} True {Style.RESET_ALL}\n')
    input('Press Enter to continue...')

if black_frame:
    #black_frames_check
    add_black_frames = black_frame_check(role, title)
    if add_black_frames:
        fadeout_start_video, fadeout_start_audio = fadeout_position(title)
        print(f'\nAdd Black Frames: {Back.GREEN}{Fore.BLACK} True {Style.RESET_ALL}\n')
        # fix_black_frames(title, ffmpeg_add_bf)
    input('Press Enter to continue...')



if audio:
    # audio analysis
    analysis(audiocheck, title)
    audio_results(temp_output)
    
    fix_audio_levels = input_validator("Do you want to fix the audio? y/n", "yes", "y", "no", "n")
    if fix_audio_levels:
        print(f'\nFix the audio levels: {Back.GREEN}{Fore.BLACK} True {Style.RESET_ALL}\n')

        # Fix the audio. The code varies depending if the video is stereo or dual mono

        # if channels == "stereo":
        #     audio_fix(title, audio_levels['measured_i'], audio_levels['measured_tp'], audio_levels['measured_lra'], audio_levels['measured_thresh'], "dual_mono=false", ffmpeg_audio_fix)
        # elif channels == "dual mono":
        #     audio_fix(title, audio_levels['measured_i'], audio_levels['measured_tp'], audio_levels['measured_lra'], audio_levels['measured_thresh'], "dual_mono=true", ffmpeg_audio_fix)

    input('Press Enter to continue...')

ffmpeg_code = ""


# ## OLD VERSION - New one starts after the comment block
# # remove timecode track
# if remove_timecode_track:
#     ffmpeg_code = only_remove_timecode_track.format(source=title, fixed_output=fixed_output)
#     # remove timecode track and add black frames
#     if add_black_frames:
#         ffmpeg_code = add_black_frames_remove_timecode.format(source=title, start_of_fadeout_video=fadeout_start_video, start_of_fadeout_audio=fadeout_start_audio, fixed_output=fixed_output)
#         # remove timecode track, add black frames and fix audio
#         if fix_audio_levels:
#             ffmpeg_code = ffmpeg_remove_timecode_add_black_frames_fix_audio.format(source=title, start_of_fadeout_video=fadeout_start_video, start_of_fadeout_audio=fadeout_start_audio, integrated=audio_levels['measured_i'], true_peak=audio_levels['measured_tp'], lra=audio_levels['measured_lra'], threshold=audio_levels['measured_thresh'], dual_mono=dual_mono, fixed_output=fixed_output)
#     # remove timecode track and fix audio
#     elif fix_audio_levels and not add_black_frames:
#         ffmpeg_code = remove_timecode_and_fix_audio.format(source=title, integrated=audio_levels['measured_i'], true_peak=audio_levels['measured_tp'], lra=audio_levels['measured_lra'], threshold=audio_levels['measured_thresh'], dual_mono=dual_mono, fixed_output=fixed_output)
# # add black frames
# elif add_black_frames and not remove_timecode_track:
#     ffmpeg_code = ffmpeg_add_black_frames.format(source=title, start_of_fadeout_video=fadeout_start_video, start_of_fadeout_audio=fadeout_start_audio,fixed_output=fixed_output)
#     # add black frames and fix audio levels
#     if fix_audio_levels:
#         ffmpeg_code = ffmpeg_add_black_frames_and_fix_audio.format(source=title, start_of_fadeout_video=fadeout_start_video, start_of_fadeout_audio=fadeout_start_audio, integrated=audio_levels['measured_i'], true_peak=audio_levels['measured_tp'], lra=audio_levels['measured_lra'], threshold=audio_levels['measured_thresh'], dual_mono=dual_mono, fixed_output=fixed_output)
#
# # only fix audio levels
# elif fix_audio_levels and not add_black_frames and not remove_timecode_track:
#     ffmpeg_code = ffmpeg_audio_fix.format(source=title, integrated=audio_levels['measured_i'], true_peak=audio_levels['measured_tp'], lra=audio_levels['measured_lra'], threshold=audio_levels['measured_thresh'], dual_mono=dual_mono, fixed_output=fixed_output)
#


fix_key = what_to_fix([remove_timecode_track, "remove_timecode_track"], 
                      [add_black_frames, "add_black_frames"], 
                      [fix_audio_levels, "fix_audio_levels"],
                      [remove_dup_frames, "remove_duplicate_frames"])

ffmpeg_options = {
        "remove_timecode_track" : only_remove_timecode_track.format(source=title, fixed_output=fixed_output),

        "add_black_frames" : ffmpeg_add_black_frames.format(source=title, start_of_fadeout_video=fadeout_start_video, start_of_fadeout_audio=fadeout_start_audio,fixed_output=fixed_output),

        "fix_audio_levels" : ffmpeg_audio_fix.format(source=title, integrated=audio_levels['measured_i'], true_peak=audio_levels['measured_tp'], lra=audio_levels['measured_lra'], threshold=audio_levels['measured_thresh'], dual_mono=dual_mono, fixed_output=fixed_output),

        "remove_timecode_track-add_black_frames" : add_black_frames_remove_timecode.format(source=title, start_of_fadeout_video=fadeout_start_video, start_of_fadeout_audio=fadeout_start_audio, fixed_output=fixed_output),

        "remove_timecode_track-add_black_frames-fix_audio_levels" : ffmpeg_remove_timecode_add_black_frames_fix_audio.format(source=title, start_of_fadeout_video=fadeout_start_video, start_of_fadeout_audio=fadeout_start_audio, integrated=audio_levels['measured_i'], true_peak=audio_levels['measured_tp'], lra=audio_levels['measured_lra'], threshold=audio_levels['measured_thresh'], dual_mono=dual_mono, fixed_output=fixed_output),

        "remove_timecode_track-fix_audio_levels" : remove_timecode_and_fix_audio.format(source=title, integrated=audio_levels['measured_i'], true_peak=audio_levels['measured_tp'], lra=audio_levels['measured_lra'], threshold=audio_levels['measured_thresh'], dual_mono=dual_mono, fixed_output=fixed_output),

        "add_black_frames-fix_audio_levels" : ffmpeg_add_black_frames_and_fix_audio.format(source=title, start_of_fadeout_video=fadeout_start_video, start_of_fadeout_audio=fadeout_start_audio, integrated=audio_levels['measured_i'], true_peak=audio_levels['measured_tp'], lra=audio_levels['measured_lra'], threshold=audio_levels['measured_thresh'], dual_mono=dual_mono, fixed_output=fixed_output),
        
        "remove_duplicate_frames" : remove_duplicate_frames.format(source=title, cycle_int=duplicate_frames, fixed_output=remove_dp_output)

        }
try:
    ffmpeg_code = ffmpeg_options[fix_key]
except:
    ffmpeg_code = False
    print("\nEverything looks great, nothing to fix here 🎉")

if ffmpeg_code:
    ffmpeg_fix(ffmpeg_code)
    print(f'\nCheck the {Fore.CYAN}line of ffmpeg{Style.RESET_ALL} I used to fix your title:\n {Back.BLACK}{Fore.GREEN}{ffmpeg_code}{Style.RESET_ALL} ')



print('\nEnd of the review\n')
