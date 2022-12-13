#!/usr/bin/env python3

import time
from colorama import Fore, Style
from analyze import *
from meta import *
from black_frames import *
from settings import *
from audio import *
from actions import *





    # THE APP STARTS INTERACTING HERE.


if __name__ == '__main__':

    print("\nBefore we start I need some information.\n")
    
    title = input("Drag your file here: ").replace(' ', '')

    main_prev = input_validator("Is your title main[m] or preview[p]?", "main", "m", "preview", "p")
    stereo_or_dm = input_validator("Is your title stereo[s] or dual mono[dm]?", "stereo", "s", "dual mono", "dm")

    if (main_prev == "m") or (main_prev == "main"):
        main_prev = "main"
    else:
        main_prev = "preview"

    if (stereo_or_dm == "s") or (stereo_or_dm == "stereo"):
        stereo_or_dm = "stereo"
    else:
        stereo_or_dm = "dual mono"

    print(f"\n\t{Fore.CYAN}The video role is:{Style.RESET_ALL} {main_prev}\n\t{Fore.CYAN}The audio is:{Style.RESET_ALL} {stereo_or_dm}\n\t{Fore.CYAN}The location is:{Style.RESET_ALL} {title}")

    print("\nWe are ready to start.\n")
    
    time.sleep(0.2)


    # Function to ask if the user wants to check the video metadata
    metadata_analysis = want_to_analyze("video metadata", "meta_checker", title)

    
    # Function to ask if the user wants to check for black frames
    bf_check = input_validator("Do you want to search for black frames? y/n", "yes", "y", "no", "n")
    if bf_check:
        time.sleep(0.2)
        black_frame_check(main_prev, title)


    # Function to ask if the user wants to check the audio
    audio_analysis = want_to_analyze("audio", "audio_checker", title)
    if audio_analysis == True:

        want_fix_audio = input_validator("Do you want to fix the audio? y/n", "yes", "y", "no", "n")
        if want_fix_audio:
            time.sleep(0.2)
            # Fix the audio. The code varies depending if the video is stereo or dual mono
            if stereo_or_dm == "stereo":
                audio_fix(title, audio_levels['measured_i'], audio_levels['measured_tp'], audio_levels['measured_lra'], audio_levels['measured_thresh'], "dual_mono=false", ffmpeg_audio_fix)
            elif stereo_or_dm == "dual mono":
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


    print("Review Ended")
    input("Press intro to end the session. \n")
    exit

