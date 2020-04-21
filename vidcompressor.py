import moviepy.editor as mp
from randstr import randstr
import os


def get_new_filename(path):
    return randstr(11) + ".mp4"


def compress(bit, f, dirs="", savedir=""):
    BR = str(bit) + "k"
    video_compressed = mp.VideoFileClip(dirs + f)
    new_file = get_new_filename(f)
    video_compressed.write_videofile(
        savedir + new_file, bitrate=BR, verbose=False, codec="mpeg4", audio_codec='aac')
    return new_file
