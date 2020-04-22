<img align="right" alt="icon" src="favicons/android-chrome-192x192.png" height="150px">

# Quickskits
make easy and quick videos

# about it
quickskits is a social media plateform based on the popular social media Tiktok with its logo and layout design

# is it safe?
Yes, the website can be found on the domain [quickskits.app](https://quickskits.app/) which requires https meaning that all your traffic will go through the internet un harmed. But what about the servers, do they keep my info secure? yes, for example when you password is given to the server the password is hashed with a salt key making sure that even if your password is a common one no one can go the the account info list and and list the ones that happen to have the same password because they have to same hash.

example:

Password: `Password123`

hashed: `b938fb7dc46cd28044d860f311483b3de7a21c22be92adc29e5182da96086620ed6d40251cb82d05cc8ac5a38de97967faa4d70c6a94cab3f770d3cd91dbaf43` (what is stored on the server)

# what does it use
quickskit uses many different module, for the video editing it uses [moviepy](https://zulko.github.io/moviepy/), for the webengine it uses [flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) and many more. [more info](https://github.com/Ugric/quickskits/blob/master/requirements.txt)

# how it works

**Source code:**

[[file]](https://github.com/Ugric/quickskits/blob/master/quickskits.py) this files main module is [flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) which is frontend [Werkzeug](https://pypi.org/project/Werkzeug/). In this file it stores stuff website directorys.

**Templates folder:**

[[folder]](https://github.com/Ugric/quickskits/tree/master/templates) this folder stores all the html templates used by the Source codes [flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) module.

**Custom Login Module:**

[[folder]](https://github.com/Ugric/quickskits/tree/master/logindatabase) this module stores the info on the users, for example, usernames, hashed with salt passwords, cookie storing, UUIDs, user email addresses, the ability to add an account, login with the choice of either the username or the email address and to logout (**more features will be added in the future**)
