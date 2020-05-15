from login import *
from password_strength import PasswordStats, PasswordPolicy
from randstr import randstr
import json
from datetime import datetime
import os
import bleach


class loginBaseSetup:
    def __init__(self, loginstoredname):
        self.loginstoredname = loginstoredname
        try:
            self.loginbase = json.load(open(os.path.join(os.path.dirname(
                __file__), self.loginstoredname+".json"), "r"))
        except Exception as e:
            print(str(e))
            open(os.path.join(os.path.dirname(
                __file__), self.loginstoredname+".json"), "w").write("[]")
            self.loginbase = []
        self.policy = PasswordPolicy.from_names(length=5,
                                                numbers=1,)
        set_salt(
            "1811ccff35d7a09bb2adf7236fecb10e3bad48c460e6b270a60dc3427812abc75e3a45bbd10f8bf397c69e1c84a46760a26efbdf992f45a5be292e65bd6212e8"
        )

    def check(self, password):
        neededletter = self.policy.test(password)
        if neededletter == []:
            return True
        else:
            output = ""
            neededletterlen = len(neededletter)
            xletter = 0
            for i in neededletter:
                if neededletterlen - xletter >= 3:
                    output += str(i) + ", "
                elif neededletterlen - xletter >= 2:
                    output += str(i) + " and "
                else:
                    output += str(i) + "."
                xletter += 1
            return "the password needs: " + output

    def adddata(self, jsons):
        self.loginbase.append(jsons)
        open(os.path.join(os.path.dirname(
            __file__), self.loginstoredname+".json"), "w").write(json.dumps(self.loginbase))

    def checknotifications(self, uuid):
        for user in self.loginbase:
            if user["uuid"] == uuid:
                if "notification" not in user:
                    user["notification"] = []
                    open(os.path.join(os.path.dirname(
                        __file__), self.loginstoredname+".json"), "w").write(json.dumps(self.loginbase))
                if user["notification"] != []:
                    jsonnotification = user["notification"][0]
                    if user["notification"][0]["new"] == True:
                        jsonnotification["new"] = True
                    user["notification"].remove(user["notification"][0])
                    return jsonnotification
                else:
                    return {"new": False}
        return {"new": False}

    def addnotification(self, uuid, notificationjson):
        for user in self.loginbase:
            if user["uuid"] == uuid:
                user["notification"].append(notificationjson)
                return True
        return False

    def verify(self, verificationkey):
        for login in self.loginbase:
            if datetime.timestamp(datetime.now()) - login["timestamp"] >= 3600 and login["verified"] != 1:
                self.loginbase.remove(login)
                open(os.path.join(os.path.dirname(
                    __file__), self.loginstoredname+".json"), "w").write(json.dumps(self.loginbase))
            if login["verificationkey"] == verificationkey and login["verified"] != 1:
                login["verified"] = 1
                open(os.path.join(os.path.dirname(
                    __file__), self.loginstoredname+".json"), "w").write(json.dumps(self.loginbase))
                return True
        return "this verification code is not on our servers."

    def getuserinfofromuuid(self, uuid):
        for user in self.loginbase:
            if user["uuid"] == uuid:
                return user
        return False

    def getuserinfofromusername(self, username):
        for user in self.loginbase:
            if user["user"] == username:
                return user
        return False

    def addlogin(self, username, password, email):
        passwordtested = self.check(password)
        if passwordtested == True:
            for login in self.loginbase:
                if login["user"].upper() == username.upper():
                    return {"failed": f"the username '{username}' already taken"}
                if login["email"].upper() == email.upper():
                    return {"failed": f"the email address '{email}' already being used on another account"}
            tempjson = {}
            tempjson["user"] = bleach.clean(username)
            tempjson["salt"] = randstr(100)
            tempjson["password"] = generate_password_hash(
                password+tempjson["salt"])
            tempjson["email"] = email
            tempjson["uuid"] = randstr(40)
            tempjson["token"] = randstr(30)
            tempjson["verified"] = 0
            tempjson["notifications"] = {"new": False}
            tempjson["timestamp"] = datetime.timestamp(datetime.now())
            tempjson["verificationkey"] = randstr(50)
            self.adddata(tempjson)
            return {"token": tempjson["token"], "verificationkey": tempjson["verificationkey"]}
        else:
            return {"failed": passwordtested}

    def logout(self, cookie):
        for login in self.loginbase:
            if login["token"] == cookie:
                login["token"] = randstr(30)
                open(os.path.join(os.path.dirname(
                    __file__), self.loginstoredname+".json"), "w").write(json.dumps(self.loginbase))
                return True
        return False

    def login(self, usernameEmail, password):
        for login in self.loginbase:
            if login["user"] == usernameEmail and login["password"] == generate_password_hash(password+login["salt"]) or login["email"] == usernameEmail and login["password"] == generate_password_hash(password+login["salt"]):
                if login["verified"] == 1:
                    login["token"] = randstr(30)
                    open(os.path.join(os.path.dirname(
                        __file__), self.loginstoredname+".json"), "w").write(json.dumps(self.loginbase))
                    return login
                else:
                    return {"failed": "you need to verify your account by your email. your account will be deleted after 1 hour of the account being made unless the account is verified."}
        return {"failed": "incorrect username / email or password."}

    def checktoken(self, token):
        for login in self.loginbase:
            if login["token"] == token and login["verified"] == 1:
                return login
        return False
