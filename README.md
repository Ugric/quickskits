<img align="right" alt="icon" src="favicons/android-chrome-192x192.png" height="150px">

# Quickskits
make easy and quick videos

# about it
quickskits is a social media plateform based on the popular social media Tiktok with its logo and layout design

# is it safe?
Yes, the website can be found on the domain [quickskits.app](https://quickskits.app/) which requires https meaning that all your traffic will go through the internet un harmed. But what about the servers, do they keep my info secure? yes, for example when you password is given to the server the password is hashed with a salt key making sure that even if your password is a common one no one can go the the account info list and and list the ones that happen to have the same password because they have to same hash.

example:

Password: `Password123`

salt: `randomstring`

hash(password+salt): `48d8d064db1456ccb3cc5697fb3014ee90808e4a7da45d3ce214f9f6db0bacabc75253a43669e05970ee5eaca0c8ff875e84b910f6e115613805b2a6c7a6414f` (what is stored on the server)

# what does it use
quickskit uses many different module, for the video editing it uses [moviepy](https://zulko.github.io/moviepy/), for the webengine it uses [flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) and many more. [more info](https://github.com/Ugric/quickskits/blob/master/requirements.txt)

# how it works

**Source code:**

[[file]](https://github.com/Ugric/quickskits/blob/master/quickskits.py) this files main module is [flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) which is frontend [Werkzeug](https://pypi.org/project/Werkzeug/). In this file it stores stuff website directorys.

**Templates folder:**

[[folder]](https://github.com/Ugric/quickskits/tree/master/templates) this folder stores all the html templates used by the Source codes [flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) module.

**Custom Login Module:**

[[folder]](https://github.com/Ugric/quickskits/tree/master/logindatabase) this module stores the info on the users, for example, usernames, hashed with salt passwords, cookie storing, UUIDs, user email addresses, the ability to add an account, login with the choice of either the username or the email address and to logout (**more features will be added in the future**) [more info](#custom-login-module-extra-info)

# Custom Login Module (extra info)
[[addlogin(self, username, password, email)]](https://github.com/Ugric/quickskits/blob/master/logindatabase/__init__.py) when signing up the user is required to input a **Username**, **email address** and **password** (the source code deals with the retype password), the module then makes sure the password is secure enough to be allowed to be the password, after this complete the account is created (**hashes the password with a salt**), however will have to be verified (**e.g. email**), the function response json, verificationkey: a string of 50 random letters to be used to verify the account in the chosen way, and token: the cookie stored on the users device to identify the user.

[[verify(self, verificationkey)]](https://github.com/Ugric/quickskits/blob/master/logindatabase/__init__.py) when this function is given the varificationkey from the signup function it will verify the account.

[[checktoken(self, token)]](https://github.com/Ugric/quickskits/blob/master/logindatabase/__init__.py) when this module is given a token, if the token is not valid it will respond with False, however if the token is valid it will respond the the user info (**e.g. username, uuid, hashed password...**)
