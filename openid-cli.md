
from https://ssb22.user.srcf.net/setup/openid-cli.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/setup/openid-cli.html) just in case)

# OpenID with command-line authorisation

Some “blog” (Web log) platforms require OpenID if you wish to leave your name and URL on a comment. Although many OpenID providers verify you in-browser, OpenID was originally designed to be compatible with out-of-browser verification methods too (e.g. the server calls you by telephone and asks for a one-time code to show it *was* you who just tried to log in), and this kind of approach doesn’t seem to have been used as much.

For Unix or GNU/Linux users with home server equipment, the obvious setup is an OpenID server running in a terminal window (on the desktop or Linux console, or over SSH), and asking its questions via that terminal. It’s out-of-browser verification and you don’t need a telephony service. The main disadvantage is it cannot be used on platforms that restrict themselves to a small number of well-known OpenID providers instead of allowing everybody to run one.

This simple script [openid-cli.py](openid-cli.py) can be used with `python-openid`. It expects a file called `openid_config.py` containing something like:

`local_addr = ('localhost', 8100)

public_endpoint_url = "http://home-server.example.org/openid"

profile = { "fullname":"A. N. Other", "nickname":"A.N.O." }`

and in your home server’s `/etc/nginx/sites-enabled/default` (or equivalent for Apache),

`location /openid {

proxy_pass http://localhost:8100;

}`

so that requests for `/openid` are sent to the script. Running the script will then prompt you to add the correct markup to your home page’s `<head>` section, whereupon you should be able to use your home page’s URL as an OpenID logon and confirm in the terminal.

(You do not have to keep the script running at times when you’re not expecting to use OpenID, nor do you have to keep the markup in your home page’s `<head>` section at other times. You should be able to set this up as a ‘one-off’ to log in to something via OpenID, and take it down again afterwards.)

## https trouble

Some providers (e.g. BlogSpot in 2017) assume they can put `https` instead of `http` at the start when sending your browser to a ‘checkid_setup’ URL (and they don’t do ‘checkid_immediate’), so, if your nginx doesn’t do HTTPS, you’ll have to delete the `s` in your browser’s address bar when it tries to load an `https` page from your home server. (The security of that request is irrelevant if the whole point of this setup is to ask you the important question *in the terminal* not the browser.)

If using the default port 80 for HTTP traffic, you may wish to ensure your home server’s firewall allows a proper ‘closed’ response on port 443 so the browser doesn’t wait too long trying to load the `https` page before presenting you with the error condition and letting you edit the URL. (If you are using a port other than 80, a provider that assumes `https` will have your browser attempt HTTPS negotiations on that alternate port, likely creating needless clutter in your logs.)

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Apache is a registered trademark of The Apache Software Foundation, which from February to July 2023 acknowledged the Chiricahua Apache, the Choctaw Apache, the Fort Sill Apache, the Jicarilla Apache, the Mescalero Apache, the Lipan Apache, the Apache Tribe of Oklahoma, the Plains Apache, the San Carlos Apache, the Tonto Apache, the White Mountain Apache, the Yavapai Apache and the Apache Alliance.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
OpenID is a registered trademark of the OpenID Foundation.
Unix is a trademark of The Open Group.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
