import requests
import json
import threading
url = "http://127.0.0.1:4141/"


class QuickskitsApiError(Exception):
    pass


class startapi:
    def __init__(self, u, p):
        print("logging in...")
        try:
            r = requests.post(url+"api/login", data={"u": u, "p": p})
        except Exception as e:
            raise ConnectionError(e)
        print("sent login request.")
        responsejson = r.json()
        if "token" in responsejson:
            self.token = responsejson["token"]
        else:
            raise QuickskitsApiError(responsejson["error"])

    def uploadvideo(self, videodirs, title, description, music, mixer=None, portrat=0):
        print("processing...")
        if music != "none" and mixer == None:
            raise ValueError("mixer has to be set when music is not none")
        if music == "none":
            music = "n"
            mixer = 0
        files = []
        for videodir in videodirs:
            files.append(('file', open(videodir, 'rb')))
        print("sending request to the server and getting server to render...")
        if portrat == True:
            portrat = "protrat"
        try:
            r = requests.post(url+"api/upload", files=files, data={
                "token": self.token, "title": title, "description": description, "music": music, "mixer": mixer})
        except Exception as e:
            raise ConnectionError(e)
        print("sent!")
        responsejson = r.json()
        if "OK" in responsejson:
            return responsejson["path"]
        else:
            raise QuickskitsApiError(responsejson["error"])

    def getrecommendation(self):
        try:
            r = requests.post(url+"api/recommended",
                              data={"token": self.token})
        except Exception as e:
            raise ConnectionError(e)
        responsejson = r.json()
        if "OK" in responsejson:
            return responsejson["recommended"]
        else:
            raise QuickskitsApiError(responsejson["error"])

    def getchat(self, username):
        try:
            r = requests.post(url+"api/getchat",
                              data={"token": self.token, "user": username})
        except Exception as e:
            raise ConnectionError(e)
        responsejson = r.json()
        if "r" in responsejson:
            return responsejson["r"]
        else:
            raise QuickskitsApiError(responsejson["error"])

    def messageuser(self, username, message):
        if message == "":
            return True
        try:
            r = requests.post(url+"api/message",
                              data={"token": self.token, "user": username, "message": message})
        except Exception as e:
            raise ConnectionError(e)
        responsejson = r.json()
        if responsejson["r"] == True:
            return responsejson["r"]
        else:
            raise QuickskitsApiError(responsejson["error"])
