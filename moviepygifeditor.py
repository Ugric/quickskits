from moviepy.editor import *
from randstr import randstr
import moviepy.video.fx.all as vfx


def boomerang(video, savedir, portat):
    clip = VideoFileClip(video)
    if portat == "portat":
        clip = clip.resize((180, 240))
    else:
        clip = clip.resize(width=240)
    sub = clip.subclip(1, 0)
    clip2 = sub.speedx(final_duration=1)
    clip3 = clip2.fx(vfx.time_mirror)
    final = concatenate_videoclips([clip2, clip3])
    filesaveas = randstr(15)
    final.to_gif(savedir+filesaveas+".gif", fps=10)
    clip.close()
    return filesaveas+".gif"
