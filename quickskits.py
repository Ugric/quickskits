import videoai
from moviepygifeditor import boomerang
from werkzeug import secure_filename
import vidcompressor
import bleach
import sys
import os
import threading
import smtplib
from datetime import datetime
from requests import get
from flask import (
    Flask,
    redirect,
    request,
    render_template,
    send_file,
    url_for,
    send_from_directory,
    stream_with_context,
    Response,
    make_response,
    jsonify,
)
import render
import random
from randstr import randstr
import glob
import logindatabase
import json
import time
from millify import millify
import random
print("quickskits booting up...")

serverurl = "https://quickskits.app/"


def verifyemail(email, username, link):
    gmail_user = 'noreply.quickskits@gmail.com'
    gmail_password = 'quickskitspassword123'
    sent_from = gmail_user
    to = [email]
    subject = 'verify its you'
    body = f'''hello {email},
    a quickskits account was registered under your email.

    account info:
    username: {username}

    verify email:
    {link}

    from,
        Quickskits (noreply.quickskits@gmail.com)'''

    email_text = """\
From: %s
To: %s
Subject: %s

%s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')


files = glob.glob("temp/*")
for f in files:
    os.remove(f)

app = Flask("__main__", static_url_path="")
try:
    lastvideo = json.load(open(os.path.join(os.path.dirname(
        __file__), "videos/lastvideos.json"), "r"))
except:
    open(os.path.join(os.path.dirname(
        __file__), "videos/lastvideos.json"), "w").write("[]")
    lastvideo = []

try:
    errorlog = json.load(open(os.path.join(os.path.dirname(
        __file__), "error.log"), "r"))
except:
    open(os.path.join(os.path.dirname(
        __file__), "error.log"), "w").write("[]")
    errorlog = []
"""vpnlist = vpndetector.startIpTester("blockedIps")"""
alreadyuploaded = []

logindatabase = logindatabase.loginBaseSetup("quickskits")

"""vpndetector.detectvpn(app, vpnlist)"""

viewsrequests = []

uploadids = []


def checkalreadyuploaded(filename):
    global alreadyuploaded
    for upload in alreadyuploaded:
        if upload == filename:
            return True
    return False


def addtoalreadyuploaded(filename):
    global alreadyuploaded
    alreadyuploaded.insert(0, filename)


@app.route("/")
def home():
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    return redirect("/latest")


@app.route("/recommended")
def recommended():
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    if 'token' not in request.cookies:
        return redirect("/login")
    else:
        if logindatabase.checktoken(request.cookies["token"]) == False:
            return redirect("/login")
    return render_template("recommended.html")


@app.route("/latest")
def trending():
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    if 'token' not in request.cookies:
        return redirect("/login")
    else:
        if logindatabase.checktoken(request.cookies["token"]) == False:
            return redirect("/login")
    return render_template("trending.html")


@app.route("/rendertemplate/<path:html>")
def html(html):
    return render_template(html)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    global serverurl
    if 'token' in request.cookies and logindatabase.checktoken(request.cookies["token"]) != False:
        return redirect("/latest")
    if request.method == "POST":
        if request.form["password"] == request.form["rpassword"]:
            if "-" not in request.form["username"]:
                loginresponse = logindatabase.addlogin(
                    request.form["username"], request.form["password"], request.form["email"])
                if "token" in loginresponse:
                    threading.Thread(target=verifyemail, args=(
                        request.form["email"], request.form["username"], serverurl+"verify/"+loginresponse["verificationkey"])).start()
                    resp = make_response(
                        render_template("server message.html", messagetitle="Success", message="check your emails to verify your account."))
                    resp.set_cookie('token', loginresponse["token"])
                    return resp
                else:
                    return render_template("signup.html",  username=request.form["username"], email=request.form["email"], error=loginresponse["failed"])
            else:
                return render_template("signup.html",  username=request.form["username"].replace("-", " "), email=request.form["email"], error="'-' is an illegal character, we have changed it to a ' '.")
        else:
            return render_template("signup.html",  username=request.form["username"], email=request.form["email"], error="password and retype password need to be the same.")

    else:
        return render_template("signup.html")


@app.route("/watch/<path:videoid>")
def watch(videoid):
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    if 'token' not in request.cookies:
        return redirect("/login")
    else:
        if logindatabase.checktoken(request.cookies["token"]) == False:
            return redirect("/login")
    return render_template("watchvideo.html", videoid=videoid)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    if 'token' in request.cookies and logindatabase.checktoken(request.cookies["token"]) != False:
        return redirect("/latest")
    if request.method == "POST":
        loginresponse = logindatabase.login(
            request.form["usernameemail"], request.form["password"])
        if "token" in loginresponse:
            resp = make_response(
                redirect("/recommended"))
            resp.set_cookie('token', loginresponse["token"])
            return resp
        else:
            return render_template("login.html",  username=request.form["usernameemail"], error=loginresponse["failed"])
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    if 'token' not in request.cookies:
        return redirect("/login")
    elif logindatabase.checktoken(request.cookies["token"]) == False:
        return redirect("/login")
    if logindatabase.logout(request.cookies["token"]):
        resp = make_response(redirect("/login"))
        resp.set_cookie('token', expires=0)
        return resp
    else:
        return render_template("server message.html", messagetitle="Error", message="error logging out.")


@app.route("/verify/<path:token>", methods=["GET", "POST"])
def verify(token):
    verifyresponse = logindatabase.verify(token)
    if verifyresponse == True:
        return render_template("server message.html", messagetitle="Success", message="the account was verified.")
    else:
        return render_template("server message.html", messagetitle="Error", message=verifyresponse)


@app.route("/boomerrang/<path:files>")
def getboomerrang(files):
    if 'token' not in request.cookies:
        return redirect("/login")
    return send_from_directory("videogif", files)


@app.route("/serverimagedata/<path:files>")
def templates(files):
    return send_from_directory("serverimagedata", files)


@app.route("/checklogin")
def checklogin():
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    if 'token' not in request.cookies:
        return "false"
    elif logindatabase.checktoken(request.cookies["token"]) == False:
        return "false"
    else:
        return "true"


@app.route("/favicon/<path:files>")
def favicons(files):
    return send_from_directory("favicons", files)


@app.route("/user")
def userprofile():
    user = request.args["user"].replace("-", " ")
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    userinfo = logindatabase.getuserinfofromusername(user)
    output = []
    if userinfo != False:
        return render_template("profile.html", username=user)
    else:
        return "the user '"+user+"' could not be found on our servers."


@app.route("/user/getvideos")
def userprofilejson():
    user = request.args["user"].replace("-", " ")
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    userinfo = logindatabase.getuserinfofromusername(user)
    output = []
    if userinfo != False:
        for video in lastvideo:
            if video["uuid"] == userinfo["uuid"]:
                output.append(
                    {"boomerrang": video['boomerrang'], "title": video['title'], "views": millify(video["views"]), "src": "/watch/"+video["videoid"], "likes": len(video["likedlist"])})
        return jsonify(output)
    else:
        return jsonify([{"error": "the user '"+user+"' could not be found on our servers."}])


@app.route("/getjson/<path:video>/<path:number>")
def getjsonlatest(video, number):
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    if 'token' not in request.cookies:
        return redirect("/login")
    else:
        if logindatabase.checktoken(request.cookies["token"]) == False:
            return redirect("/login")
    if video == "latest":
        viewerinfo = logindatabase.checktoken(request.cookies["token"])
        finishedvideo = []
        for latestvideo in lastvideo:
            userinfo = logindatabase.getuserinfofromuuid(
                latestvideo["uuid"])
            video = {}
            video["src"] = latestvideo["src"]
            video["title"] = latestvideo["title"]
            video["description"] = latestvideo["description"]
            video["stretch"] = latestvideo["stretch"]
            video["videoid"] = latestvideo["videoid"]
            video["views"] = millify(latestvideo["views"])
            video["videoliked"] = "false"
            if viewerinfo["uuid"] in latestvideo["likedlist"]:
                video["videoliked"] = "true"
            video["likes"] = len(latestvideo["likedlist"])
            video["username"] = userinfo["user"]
            finishedvideo.append(video)
        return jsonify(finishedvideo)
    elif video == "video":
        viewerinfo = logindatabase.checktoken(request.cookies["token"])
        videox = 0
        for video in lastvideo:
            if video["videoid"] == number:
                userinfo = logindatabase.getuserinfofromuuid(
                    lastvideo[int(videox)]["uuid"])
                video = {}
                video["src"] = lastvideo[int(videox)]["src"]
                video["title"] = lastvideo[int(videox)]["title"]
                video["description"] = lastvideo[int(videox)]["description"]
                video["stretch"] = lastvideo[int(videox)]["stretch"]
                video["videoid"] = lastvideo[int(videox)]["videoid"]
                video["views"] = millify(lastvideo[int(videox)]["views"])
                video["videoliked"] = "false"
                for likeduser in lastvideo[int(videox)]["likedlist"]:
                    if likeduser == viewerinfo["uuid"]:
                        video["videoliked"] = "true"
                video["likes"] = len(lastvideo[int(videox)]["likedlist"])
                video["username"] = userinfo["user"]
                return jsonify(video)
            videox += 1
        return jsonify(
            {
                "src": "/videos/endofquickskits",
                "title": "quickskits",
                "description": "you have found the end of quickskits, well done!",
                "stretch": 0,
                "views": "0",
                "username": "quickskits",
                "videoid": "error",
                "videoliked": "false",
                "likes": 0,
            }
        )
    elif video == "recommended":
        try:
            viewerinfo = logindatabase.checktoken(request.cookies["token"])
            recommendedvideos = videoai.getrecommended(viewerinfo, lastvideo)
            finishedvideo = []
            for recommendedvideo in recommendedvideos:
                userinfo = logindatabase.getuserinfofromuuid(
                    recommendedvideo["uuid"])
                video = {}
                video["src"] = recommendedvideo["src"]
                video["title"] = recommendedvideo["title"]
                video["description"] = recommendedvideo["description"]
                video["stretch"] = recommendedvideo["stretch"]
                video["videoid"] = recommendedvideo["videoid"]
                video["views"] = millify(recommendedvideo["views"])
                video["videoliked"] = "false"
                if viewerinfo["uuid"] in recommendedvideo["likedlist"]:
                    video["videoliked"] = "true"
                video["likes"] = len(recommendedvideo["likedlist"])
                video["username"] = userinfo["user"]
                finishedvideo.append(video)
            return jsonify(finishedvideo)
        except:
            return jsonify(
                {
                    "src": "/videos/endofquickskits",
                    "title": "quickskits",
                    "description": "you have found the end of quickskits, well done!",
                    "stretch": 0,
                    "username": "quickskits",
                    "videoid": "error",
                    "videoliked": "false",
                    "likes": 0,
                }
            )
    else:
        return "unknown request", 404


@app.route("/likebutton/<path:likeunlike>/<path:videoid>")
def like(videoid, likeunlike):
    if request.user_agent.platform == "windows":
        return render_template("quickskitsindex.html")
    if 'token' not in request.cookies:
        return redirect("/login")
    else:
        if logindatabase.checktoken(request.cookies["token"]) == False:
            return redirect("/login")
    if videoid != "error":
        userinfo = logindatabase.checktoken(request.cookies["token"])
        if likeunlike == "like":
            for video in lastvideo:
                if video["videoid"] == videoid:
                    video["likedlist"].append(userinfo["uuid"])
                    open(os.path.join(os.path.dirname(
                        __file__), "videos/lastvideos.json"), "w").write(json.dumps(lastvideo))
                    return "true"
        elif likeunlike == "unlike":
            for video in lastvideo:
                if video["videoid"] == videoid:
                    if userinfo["uuid"] in video["likedlist"]:
                        video["likedlist"].remove(userinfo["uuid"])
                        open(os.path.join(os.path.dirname(
                            __file__), "videos/lastvideos.json"), "w").write(json.dumps(lastvideo))
                    return "true"
        elif likeunlike == "getlikes":
            for video in lastvideo:
                if video["videoid"] == videoid:
                    return jsonify({"likes": len(video["likedlist"])})
    return "false"


@app.route("/view/<path:videoid>")
def views(videoid):
    if request.user_agent.platform == "windows":
        return 'false'
    if 'token' not in request.cookies:
        return "false"
    elif logindatabase.checktoken(request.cookies["token"]) == False:
        return "false"
    else:
        for viewsrequest in viewsrequests:
            if viewsrequest["token"] == request.cookies["token"]:
                if viewsrequest["videoid"] == videoid and datetime.timestamp(datetime.now()) - viewsrequest["timestamp"] < 5:
                    viewsrequests.remove(viewsrequest)
                    return "false"
                else:
                    viewsrequests.remove(viewsrequest)
        viewrequestjson = {
            "token": request.cookies["token"], "viewid": randstr(11), "videoid": videoid, "timestamp": datetime.timestamp(datetime.now())}
        viewsrequests.append(viewrequestjson)
        time.sleep(random.randint(5, 10))
        if viewrequestjson in viewsrequests:
            for video in lastvideo:
                if video["videoid"] == videoid:
                    video["views"] += 1
                    return "true"
            return "false"
        else:
            return "false"


@app.route("/videos/<path:video>")
def send_video(video):
    if 'token' not in request.cookies:
        return redirect("/login")
    else:
        if logindatabase.checktoken(request.cookies["token"]) == False:
            return redirect("/login")
    global lastvideo
    try:
        return send_from_directory("videos", video)
    except:
        return send_from_directory("videoassets", "quickskitsoliveintro.mp4")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    try:
        if 'token' not in request.cookies:
            return redirect("/login")
        else:
            if logindatabase.checktoken(request.cookies["token"]) == False:
                return redirect("/login")
        userdata = logindatabase.checktoken(request.cookies["token"])
        if request.method == "POST":
            if request.form["uploadid"] in uploadids:
                return render_template("server message.html", messagetitle="Error", message="This video is already been uploaded.")
            uploadids.append(request.form["uploadid"])
            global lastvideo
            videoid = randstr(30)
            files = request.files.getlist("video")
            try:
                portat = request.form["portat"]
            except:
                portat = 0
            music = request.form["music"]
            if music == "n":
                music = False
            mixer = int(request.form["mixer"])
            if len(files) == 1:
                f = files[0]
                filename, file_extension = os.path.splitext(f.filename)
                savedir = randstr(10) + file_extension
                if checkalreadyuploaded(savedir):
                    return render_template("server message.html", messagetitle="Error", message="this video has already been uploaded try a different one.")
                else:
                    f.save("temp\\" + savedir)
                    addtoalreadyuploaded(f.filename)
                    boomerrang = boomerang(
                        "temp\\"+savedir, "videogif/", portat)
                    newfile = render.render(
                        savedir, "temp\\", portat=portat, music=music, mixer=mixer)
                    try:
                        os.remove("temp\\" + savedir)
                    except:
                        pass
                    if newfile != False:
                        conpressedversion = vidcompressor.compress(
                            10000000, newfile, dirs="temp\\", savedir="videos\\"
                        )
                        try:
                            os.remove("temp\\" + newfile)
                        except:
                            pass
                        portatsize = render.getportat(
                            "videos\\" + conpressedversion)
                        print(portatsize)
                        if portat == "portat":
                            finisheddic = {
                                "src": "/videos/" + conpressedversion,
                                "title": bleach.clean(request.form["title"]),
                                "description": bleach.clean(
                                    request.form["description"]
                                ),
                                "boomerrang": "/boomerrang/"+boomerrang,
                                "stretch": 1,
                                "uuid": userdata["uuid"],
                                "videoid": videoid,
                                "likedlist": [],
                                "views": 0,
                            }
                        else:
                            finisheddic = {
                                "src": "/videos/" + conpressedversion,
                                "title": bleach.clean(request.form["title"]),
                                "description": bleach.clean(
                                    request.form.get("description", "")
                                ),
                                "boomerrang": "/boomerrang/"+boomerrang,
                                "stretch": 0,
                                "uuid": userdata["uuid"],
                                "videoid": videoid,
                                "likedlist": [],
                                "views": 0,
                            }

                        lastvideo.insert(0, finisheddic)
                        open(os.path.join(os.path.dirname(
                            __file__), "videos/lastvideos.json"), "w").write(json.dumps(lastvideo))
                        return redirect("/watch/"+videoid)
                    else:
                        return render_template("server message.html", messagetitle="Error", message="the video was too long please upload a shorter one.")
            else:
                allfiles = []
                totallen = 0
                for f in files:
                    filename, file_extension = os.path.splitext(f.filename)
                    savedir = randstr(10) + file_extension
                    f.save("temp\\" + savedir)
                    addtoalreadyuploaded(f.filename)
                    allfiles.append(savedir)
                    totallen += render.getlength("temp\\" + savedir)
                if totallen <= 120:
                    print(allfiles)
                    boomerrang = boomerang(
                        "temp\\"+savedir, "videogif/", portat)
                    newfile = render.renderMultiple(
                        allfiles, "temp\\", portat=portat, music=music, mixer=mixer)
                    try:
                        os.remove("temp\\" + savedirs)
                    except:
                        pass
                    conpressedversion = vidcompressor.compress(
                        10000000, newfile, dirs="temp\\", savedir="videos\\"
                    )
                    try:
                        os.remove(conpressedversion)
                    except:
                        pass
                    if portat == "portat":
                        finisheddic = {
                            "src": "/videos/" + conpressedversion,
                            "title": bleach.clean(request.form["title"]),
                            "description": bleach.clean(request.form["description"]),
                            "boomerrang": "/boomerrang/"+boomerrang,
                            "stretch": 1,
                            "uuid": userdata["uuid"],
                            "videoid": videoid,
                            "likedlist": [],
                            "views": 0,
                        }
                    else:
                        finisheddic = {
                            "src": "/videos/" + conpressedversion,
                            "title": bleach.clean(request.form["title"]),
                            "description": bleach.clean(request.form["description"]),
                            "boomerrang": "/boomerrang/"+boomerrang,
                            "stretch": 0,
                            "uuid": userdata["uuid"],
                            "videoid": videoid,
                            "likedlist": [],
                            "views": 0,
                        }
                    lastvideo.insert(0, finisheddic)
                    open(os.path.join(os.path.dirname(
                        __file__), "videos/lastvideos.json"), "w").write(json.dumps(lastvideo))
                    return redirect("/watch/"+videoid)
                else:
                    return render_template("server message.html", messagetitle="Error", message="the video was too long please upload a shorter one.")

        else:
            return render_template("upload.html", uploadid=randstr(11))
    except Exception as e:
        errorlog.insert(0, {"uuid": userdata["uuid"], "error": str(e)})
        open(os.path.join(os.path.dirname(
            __file__), "error.log"), "w").write(json.dumps(errorlog))
        return render_template("server message.html", messagetitle="Error", message="there was an Error when uploading the video. either the video was corrupt or there was another issue. this error has been logged into our error.log file for futher investigation into this error.")


print("quickskits booted up.")
app.run(debug=False, host="0.0.0.0", port=4141)
