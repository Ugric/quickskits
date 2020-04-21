def getrecommended(userdata, videodata):
    likedwords = []
    for video in videodata:
        if userdata["uuid"] in video["likedlist"]:
            for word in video["title"].split():
                for likedword in likedwords:
                    if likedword["word"] == word:
                        likedword["number"] += 1
                        break
                likedwords.append({"word": word, "number": 1})
            for word in video["description"].split():
                for likedword in likedwords:
                    if likedword["word"] == word:
                        likedword["number"] += 1
                        break
                likedwords.append({"word": word, "number": 1})
    recommendedvideo = []
    for video in videodata:
        if userdata["uuid"] not in video["likedlist"]:
            for word in likedwords:
                if word["word"].upper() in video["title"].upper() or word["word"].upper() in video["description"].upper():
                    if video not in recommendedvideo:
                        recommendedvideo.append(video)
    for video in videodata:
        if userdata["uuid"] not in video["likedlist"]:
            for word in likedwords:
                if word["word"].upper() not in video["title"].upper()or word["word"].upper() not in video["description"].upper():
                    if video not in recommendedvideo:
                        recommendedvideo.append(video)
    for video in videodata:
        if userdata["uuid"] in video["likedlist"]:
            for word in likedwords:
                if word["word"].upper() in video["title"].upper() or word["word"].upper() in video["description"].upper():
                    if video not in recommendedvideo:
                        recommendedvideo.append(video)
    if likedwords == []:
        for video in videodata:
            videoinlist = 0
            if recommendedvideo == []:
                recommendedvideo.append(video)
                videoinlist = 1
            else:
                x = 0
                for recommendedvid in recommendedvideo:
                    likes = len(recommendedvid["likedlist"])
                    if likes > len(video["likedlist"]):
                        x += 1
                    else:
                        if video not in recommendedvideo:
                            recommendedvideo.insert(x, video)
                            videoinlist = 1
                        x += 1
            if videoinlist == 0:
                recommendedvideo.append(video)
    return recommendedvideo
