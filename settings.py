import random


n_output = random.randint(99999999, 99999999999)
temp_output = f"package_creation_audiolevels{n_output}.txt"




# This is a magic number, but I want to avoid the Shell=True at the beginning, so,
# index for analysis function is 2
audiocheck = {'command': ['ffmpeg', '-i', 'SOURCE', '-vn', '-filter:a', 'loudnorm=print_format=json', '-f', 'null', '-',], 'output': 'stderr'}

# index for analysis function is 7
datacheck = {'command': ['ffprobe', '-hide_banner', '-loglevel', 'warning', '-print_format', 'json', '-show_streams',  'source', ], 'output': 'stdout'}


ffmpeg_audio_fix = 'ffmpeg -i {source} -c:v copy -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags write_colr -c:a pcm_s24le -ar 48k -filter:a loudnorm=i=-24.0:tp=-6:print_format=summary:{integrated}:{true_peak}:{lra}:{threshold}:{dual_mono} {fixed_output}' 

only_remove_timecode_track = 'ffmpeg -i {source} -dn -map_metadata -1 -metadata:s:v encoder="Apple ProRes 422 HQ" -fflags bitexact -write_tmcd 0 -vendor abm0 -c copy {fixed_output}'


remove_timecode_and_fix_audio = 'ffmpeg -i {source} -dn -map_metadata -1 -metadata:s:v encoder="Apple ProRes 422 HQ" -fflags bitexact -write_tmcd 0 -vendor abm0 -c:v copy -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags write_colr -c:a pcm_s24le -ar 48k -filter:a loudnorm=i=-24.0:tp=-6:print_format=summary:{integrated}:{true_peak}:{lra}:{threshold}:{dual_mono} {fixed_output}' 


remove_duplicate_frames = ' ffmpeg -i {source} -c:v prores_ks -filter_complex decimate=cycle={cycle_int} {fixed_output}'


ffmpeg_add_black_frames = 'ffmpeg -i {source} -c:v prores_ks -vf "fade=t=in:s=1:n=4, fade=t=out:s={start_of_fadeout_video}:n=2" -af "afade=t=in:st=0:d=0.5, afade=t=out:st={start_of_fadeout_audio}:d=0.2" {fixed_output}'

add_black_frames_remove_timecode = 'ffmpeg -i {source} -dn -map_metadata -1 -c:v prores_ks -vf "fade=t=in:s=1:n=4, fade=t=out:s={start_of_fadeout_video}:n=2" -af "afade=t=in:st=0:d=0.5, afade=t=out:st={start_of_fadeout_audio}:d=0.2" {fixed_output}'


ffmpeg_add_black_frames_and_fix_audio = 'ffmpeg -i {source} -c:v prores_ks -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags write_colr -c:a pcm_s24le -ar 48k -filter_complex "[0:a]afade=t=in:st=0:d=0.5, afade=t=out:st={start_of_fadeout_audio}:d=0.2, loudnorm=i=-24.0:tp=-6:print_format=summary:{integrated}:{true_peak}:{lra}:{threshold}:{dual_mono}[out0];[0:v]fade=t=in:s=1:n=4, fade=t=out:s={start_of_fadeout_video}:n=2[out1]" -map "[out0]" -map "[out1]" {fixed_output}'



# When fixing audio and black frames at the same time we nee a special code, because we can't apply 2 filters to the same input (audio or video).
# When we add black frames we also fade-in/out the audio, so that plus audio fix is an issue
# The sollution is to create a -filter_complex code, which is a mess but it works
ffmpeg_remove_timecode_add_black_frames_fix_audio = 'ffmpeg -i {source} -c:v prores_ks -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags write_colr -c:a pcm_s24le -ar 48k -dn -map_metadata -1 -filter_complex "[0:a]afade=t=in:st=0:d=0.5, afade=t=out:st={start_of_fadeout_audio}:d=0.2, loudnorm=i=-24.0:tp=-6:print_format=summary:{integrated}:{true_peak}:{lra}:{threshold}:{dual_mono}[out0];[0:v]fade=t=in:s=1:n=4, fade=t=out:s={start_of_fadeout_video}:n=2[out1]" -map "[out0]" -map "[out1]" {fixed_output}'



ffmpeg_base = 'ffmpeg -i {source} -c:v prores_ks -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags write_colr -c:a pcm_s24le -ar 48k'

remove_tmcd = ' -dn -map_metadata -1 '

add_bfs = ' -vf "fade=t=in:s=1:n=4, fade=t=out:s={start_of_fadeout_video}:n=2" -af "afade=t=in:st=0:d=0.5, afade=t=out:st={start_of_fadeout_audio}:d=0.2" '

fix_aud = ' -filter:a loudnorm=i=-24.0:tp=-6:print_format=summary:{integrated}:{true_peak}:{lra}:{threshold}:{dual_mono} '



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







