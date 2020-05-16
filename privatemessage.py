from randstr import randstr
import json
from datetime import datetime
import datetime as date
import os
import bleach
import re
import timeago
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
            f"<a href='{url}'>{'{uri.netloc}{uri.path}'.format(uri=uriget)}</a>",
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

    def getchat(self, requestuserinfo, userinfo, number=0):
        number = int(number)
        for chat in self.privatechats:
            if chat["requestuuid"] == requestuserinfo["uuid"] and chat["useruuid"] == userinfo["uuid"] or chat["useruuid"] == requestuserinfo["uuid"] and chat["requestuuid"] == userinfo["uuid"]:
                renderjson = []
                for message in chat["messages"]:
                    if "requested" not in message:
                        message["requested"] = []
                    if message["uuid"] == userinfo["uuid"]:
                        if number != 1:
                            renderjson.append({"message": change_links(bleach.clean(
                                message["message"])), "user": "ME", "timestamp": message["timestamp"], "me": 1, "read": message["read"]})
                    else:
                        if message["read"] == "false":
                            chat["updatenumber"] += 1
                            message["read"] = "true"
                            open(os.path.join(os.path.dirname(
                                __file__), self.chat+".json"), "w").write(json.dumps(self.privatechats))
                        if number != 1 or userinfo["uuid"] not in message["requested"]:
                            renderjson.append({"message": change_links(bleach.clean(message["message"])), "user": bleach.clean(
                                requestuserinfo["user"].upper()), "timestamp": message["timestamp"], "me": 0})
                            if userinfo["uuid"] not in message["requested"]:
                                message["requested"].append(userinfo["uuid"])
                if renderjson == [] and number != 1:
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
            if chat["requestuuid"] == requestuserinfo["uuid"] and chat["useruuid"] == userinfo["uuid"] or chat["useruuid"] == requestuserinfo["uuid"] and chat["requestuuid"] == userinfo["uuid"] and message != "":
                chat["messages"].append(
                    {"uuid": userinfo["uuid"], "message": message, "timestamp": datetime.timestamp(datetime.now()), "read": "false", "requested": []})
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

    def allcontacts(self, userinfo, logindatabase):
        output = []
        for chat in self.privatechats:
            if chat["requestuuid"] == userinfo["uuid"]:
                user = logindatabase.getuserinfofromuuid(
                    chat["useruuid"])
                if chat["messages"] == []:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(
                                    user["user"]).replace(" ", "-"), "status": "0 messages"})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "0 messages"})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "0 messages"})
                elif chat["messages"][-1]["read"] != "false" and chat["messages"][-1]["uuid"] == userinfo["uuid"]:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(
                                    user["user"]).replace(" ", "-"), "status": "read", "timestamp": chat["messages"][-1]["timestamp"]})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "read", "timestamp": chat["messages"][-1]["timestamp"]})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "read", "timestamp": chat["messages"][-1]["timestamp"]})
                elif chat["messages"][-1]["read"] != "false" and chat["messages"][-1]["uuid"] != userinfo["uuid"]:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(
                                    user["user"]).replace(" ", "-"), "status": "opened", "timestamp": chat["messages"][-1]["timestamp"]})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "opened", "timestamp": chat["messages"][-1]["timestamp"]})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "opened", "timestamp": chat["messages"][-1]["timestamp"]})
                elif chat["messages"][-1]["read"] != "true" and chat["messages"][-1]["uuid"] == userinfo["uuid"]:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(
                                    " ", "-"), "status": "delivered | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "delivered | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "delivered | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})
                elif chat["messages"][-1]["read"] != "true" and chat["messages"][-1]["uuid"] != userinfo["uuid"]:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(
                                    " ", "-"), "status": "NEW MESSAGE | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "NEW MESSAGE | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "NEW MESSAGE | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})

            elif chat["useruuid"] == userinfo["uuid"]:
                user = logindatabase.getuserinfofromuuid(
                    chat["requestuuid"])
                if chat["messages"] == []:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(
                                    " ", "-"), "status": "0 messages"})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "0 messages"})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "0 messages"})
                elif chat["messages"][-1]["read"] != "false" and chat["messages"][-1]["uuid"] == userinfo["uuid"]:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(
                                    user["user"]).replace(" ", "-"), "status": "read", "timestamp": chat["messages"][-1]["timestamp"]})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "0 messages", "timestamp": chat["messages"][-1]["timestamp"]})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "read", "timestamp": chat["messages"][-1]["timestamp"]})
                elif chat["messages"][-1]["read"] != "false" and chat["messages"][-1]["uuid"] != userinfo["uuid"]:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(
                                    user["user"]).replace(" ", "-"), "status": "opened", "timestamp": chat["messages"][-1]["timestamp"]})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "0 messages", "timestamp": chat["messages"][-1]["timestamp"]})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "opened", "timestamp": chat["messages"][-1]["timestamp"]})
                elif chat["messages"][-1]["read"] != "true" and chat["messages"][-1]["uuid"] == userinfo["uuid"]:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(
                                    " ", "-"), "status": "delivered | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "0 messages", "timestamp": chat["messages"][-1]["timestamp"]})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "delivered | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})
                elif chat["messages"][-1]["read"] != "true" and chat["messages"][-1]["uuid"] != userinfo["uuid"]:
                    if output != []:
                        finished = 0
                        i = 0
                        for contact in output:
                            if chat["messages"][-1]["timestamp"] >= contact["timestamp"]:
                                finished = 1
                                output.insert(i-1, {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(
                                    " ", "-"), "status": "NEW MESSAGE | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})
                                break
                            i += 1
                        if finished == 0:
                            output.append(
                                {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "0 messages", "timestamp": chat["messages"][-1]["timestamp"]})
                    else:
                        output.append(
                            {"user": str(user["user"]), "src": "/privatemessage/?user=" + str(user["user"]).replace(" ", "-"), "status": "NEW MESSAGE | " + timeago.format(chat["messages"][-1]["timestamp"], datetime.now()), "timestamp": chat["messages"][-1]["timestamp"]})
        return output

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
