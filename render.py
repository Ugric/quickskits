import moviepy.editor as mp


def changeformat(files, formatto):
    output = ""
    for char in files:
        if char == ".":
            output += formatto
            break
        else:
            output += char
    return output


def renderMultiple(filess, dirs, portat=0, music=False, mixer=95):
    videos = []
    for files in filess:
        if portat == "portat":
            videos.append(mp.VideoFileClip(dirs + files).resize((360, 480)))
        else:
            videos.append(mp.VideoFileClip(dirs + files).resize(width=480))
    video = mp.concatenate_videoclips(videos)
    if music != False:
        musics = mp.AudioFileClip(f"videoassets/{music}.mp3")
        video = video.set_audio(mp.CompositeAudioClip([musics.volumex(
            1 - mixer/100), video.audio.volumex(mixer/100)]).set_duration(video.duration))
        video = video.set_audio(musics.set_duration(video.duration))
    intro = mp.VideoFileClip(
        "videoassets/quickskitsoliveintro.mp4").resize(video.size)
    logoimage = mp.ImageClip("videoassets/logo.png")
    logo = (
        logoimage.set_duration(video.duration)
        .resize(height=40)
        .margin(right=50, bottom=50, opacity=0)
        .set_pos(("right", "bottom"))
    )
    final = mp.CompositeVideoClip([video, logo])
    final = mp.concatenate_videoclips([final, intro.fadein(1).fadeout(1)])

    newformat = changeformat("rendered_" + files, ".mp4")
    final.write_videofile(dirs + newformat, fps=20)
    intro.close()
    logoimage.close()
    for videoss in videos:
        videoss.close()
    if music != False:
        musics.close()
    return newformat


def render(files, dirs, mixer=95, portat=0, music=False):
    videofile = mp.VideoFileClip(dirs + files)
    if portat == "portat":
        video = videofile.resize((360, 480))
    else:
        video = videofile.resize(width=480)
    if video.duration <= 120:
        if music != False:
            musics = mp.AudioFileClip(f"videoassets/{music}.mp3")
            video = video.set_audio(mp.CompositeAudioClip([musics.volumex(
                1 - mixer/100), video.audio.volumex(mixer/100)]).set_duration(video.duration))
        intro = mp.VideoFileClip("videoassets/quickskitsoliveintro.mp4").resize(
            video.size
        )
        logoimage = mp.ImageClip("videoassets/logo.png")
        logo = (
            logoimage.set_duration(video.duration)
            .resize(height=40)
            .margin(right=50, bottom=50, opacity=0)
            .set_pos(("right", "bottom"))
        )
        final = mp.CompositeVideoClip([video, logo])
        final = mp.concatenate_videoclips([final, intro.fadein(1).fadeout(1)])

        newformat = changeformat("rendered_" + files, ".mp4")
        final.write_videofile(dirs + newformat, fps=20,
                              codec="mpeg4", audio_codec='aac', threads=4)
        intro.close()
        logoimage.close()
        videofile.close()
        if music != False:
            musics.close()
        return newformat
    else:
        return False


def getlength(files):
    video = mp.VideoFileClip(files)
    filelen = video.duration
    video.close()
    return filelen


def getportat(files):
    video = mp.VideoFileClip(files)
    filelen = video.size
    print(filelen)
    video.close()
    if filelen[0] < filelen[1]:
        return True
    else:
        return False
