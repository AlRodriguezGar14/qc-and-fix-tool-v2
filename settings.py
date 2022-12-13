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


# The dictionary where the clean information goes
audio_levels = {'name':'audio levels'}
audio_analyzed = False
video_meta_analyzed = False
# This file is where I move all the information that ffmpeg prints to the console
# later it's going to be deleted, that's why I use a random generated number (not to remove anything useful)



# The dictionary with the metadata info
global video_data
video_data = {'name':'video metadata', 'timecode_track':False, 'timecode_fix':False}




