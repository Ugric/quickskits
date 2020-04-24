from randstr import randstr
import json
from datetime import datetime
import os
import bleach
import re
from urllib.parse import urlparse


def change_links(message):
    urls = re.findall(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        message,
    )
    chats = re.findall("c/(?:[a-zA-Z]|[0-9])+", message)

    output = message
    for url in urls:
        uriget = urlparse(url)
        output = output.replace(
            url,
            f"<a href='{url}' target='_blank'>{'{uri.netloc}{uri.path}'.format(uri=uriget)}</a>",
        )
    """for url in chats:
        uriget = urlparse(url)
        output = output.replace(url, f"<a href='/{url}' target='_blank'>{'{uri.netloc}{uri.path}'.format(uri=uriget)}</a>")"""
    return output


class startchats:
    def __init__(self, chat):
        self.chat = chat
        try:
            self.privatechats = json.load(open(os.path.join(os.path.dirname(
                __file__), chat+".json"), "r"))
        except:
            open(os.path.join(os.path.dirname(
                __file__), chat+".json"), "w").write("[]")
            self.privatechats = []

    def getchat(self, requestuserinfo, userinfo, number):
        for chat in self.privatechats:
            if chat["requestuuid"] == requestuserinfo["uuid"] and chat["useruuid"] == userinfo["uuid"] or chat["useruuid"] == requestuserinfo["uuid"] and chat["requestuuid"] == userinfo["uuid"]:
                renderjson = []
                for message in chat["messages"]:
                    if message["uuid"] == userinfo["uuid"]:
                        renderjson.append({"message": change_links(bleach.clean(
                            message["message"])), "user": "ME", "timestamp": message["timestamp"], "me": 1, "read": message["read"]})
                    else:
                        if message["read"] == "false":
                            chat["updatenumber"] += 1
                            message["read"] = "true"
                            open(os.path.join(os.path.dirname(
                                __file__), self.chat+".json"), "w").write(json.dumps(self.privatechats))
                        renderjson.append({"message": change_links(bleach.clean(message["message"])), "user": bleach.clean(
                            requestuserinfo["user"].upper()), "timestamp": message["timestamp"], "me": 0})
                if renderjson == []:
                    return {"chat": [{
                        "me": 0,
                        "message": "Welcome to your new chat! type a message to get started.",
                        "timestamp": 0,
                        "user": "QUICKCHAT"
                    }], "updatenumber": 0}
                return {"chat": renderjson, "updatenumber": chat["updatenumber"]}
        self.privatechats.append(
            {"useruuid": userinfo["uuid"], "requestuuid": requestuserinfo["uuid"], "messages": [], "updatenumber": 0, "requestuuidtyping": 0, "useruuidtyping": 0})
        open(os.path.join(os.path.dirname(
            __file__), self.chat+".json"), "w").write(json.dumps(self.privatechats))
        return {"chat": [{
            "me": 0,
            "message": "Welcome to your new chat! type a message to get started.",
            "timestamp": 0,
            "user": "QUICKCHAT"
        }], "updatenumber": 0}

    def addmessage(self, requestuserinfo, userinfo, message):
        for chat in self.privatechats:
            if chat["requestuuid"] == requestuserinfo["uuid"] and chat["useruuid"] == userinfo["uuid"] or chat["useruuid"] == requestuserinfo["uuid"] and chat["requestuuid"] == userinfo["uuid"]:
                chat["messages"].append(
                    {"uuid": userinfo["uuid"], "message": message.replace(":)", "🙂").replace(":(", "😔").replace("(:", "🙂").replace("):", "😔").replace("XD", "😂").replace(":D", "😃"), "timestamp": datetime.timestamp(datetime.now()), "read": "false", "new": 0})
                chat["updatenumber"] += 1
                open(os.path.join(os.path.dirname(
                    __file__), self.chat+".json"), "w").write(json.dumps(self.privatechats))
                return "true"
        return "false"

    def starttyping(self, requestuserinfo, userinfo):
        for chat in self.privatechats:
            if chat["requestuuid"] == requestuserinfo["uuid"] and chat["useruuid"] == userinfo["uuid"]:
                chat["requestuuidtyping"] = datetime.timestamp(datetime.now())
                return "true"
            elif chat["useruuid"] == requestuserinfo["uuid"] and chat["requestuuid"] == userinfo["uuid"]:
                chat["useruuidtyping"] = datetime.timestamp(datetime.now())
                return "true"
        return "false"

    def istyping(self, requestuserinfo, userinfo):
        for chat in self.privatechats:
            if chat["requestuuid"] == requestuserinfo["uuid"] and chat["useruuid"] == userinfo["uuid"]:
                if 1 >= datetime.timestamp(datetime.now()) - chat["useruuidtyping"]:
                    return "true"
                else:
                    return "false"
            elif chat["useruuid"] == requestuserinfo["uuid"] and chat["requestuuid"] == userinfo["uuid"]:
                if 1 >= datetime.timestamp(datetime.now()) - chat["requestuuidtyping"]:
                    return "true"
                else:
                    return "false"
        return "no such chat. maybe start one."
