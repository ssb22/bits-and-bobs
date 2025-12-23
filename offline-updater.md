
from https://ssb22.user.srcf.net/mwrhome/offline-updater.html
(also [mirrored on GitLab Pages](https://ssb22.gitlab.io/mwrhome/offline-updater.html) just in case)

# Offline package installation for Debian-based GNU/Linux distributions
**I have not tested this beyond Ubuntu 18.04 LTS.**

Debian, and distributions derived from it (Ubuntu, Mint, etc etc etc) use APT, which generally assumes an Internet connection.  When adding a custom set of packages to a machine without an Internet connection, it can be the case that:

1. The logistics require you to complete the job in one visit (no trips back to a connected machine to pick up a file that you didn’t realise you needed),
2. Mobile Internet in the area is too slow and/or unreliable,
3. You might not know in advance which packages are already installed on the machine,
4. It’s not feasible to carry the *complete* distribution (in its newest form) in a format readable by that machine,
5. It’s even possible that some or all of the machine’s package management infrastructure has been removed to save disk space, on the assumption that no more package management would ever have to be done.

In many cases, it suffices to install and configure the needed packages on a connected machine running the same major version of the distribution (perhaps in a virtual environment), and then create an archive of the resulting files and all dependencies, to be unpacked into the root directory on the other machine.  This [offline-updater Python 2 script](offline-updater.py) can assist with creating the archive, or simply re-downloading the deb files if the other machine’s package manager is known to be working.

The `deb` approach is likely best for `tetex` (and software that depends on it such as some versions of `lilypond`), as the maintenance this performs at installation time is not usually reflected in its file lists; you might get errors like `can't find the format file` if you try to run it without a proper installation.  There might be other packages like this too.

If you know for sure that certain versions of certain files will be available (because it will be a fresh installation, or because you’ve collected the data on your last visit), a list of these files and their timestamps can be provided so that the script will omit them; you can obtain such a list by entering `find /[belorsuv]* -type f -print0 | xargs -0 ls --full-time > existing-files` on the target machine (or on a local non-network installed copy of the fresh installation you plan).

If the machine will later be connected to the Internet in your absence, it might be easier to install some kind of remote administration.  Perhaps the simplest way to do this (which does not require setting up SSH servers, open ports or persistent connections) is to set root’s crontab to fetch commands from an HTTPS server you have an account on, e.g. `echo "@reboot wget -q -O - https://example.org/example.txt | bash" | sudo crontab -` (this will replace the existing crontab)—not suitable for very old Wget versions that did not check HTTPS certificates, but the last one of those was the 1.09 release in 2005’s Debian Sarge.

Usual disclaimers apply (I hope the above is useful, but it’s used at your own risk).

## Copyright and Trademarks
Copyright and Trademarks
All material © Silas S. Brown unless otherwise stated.
Debian is a trademark owned by Software in the Public Interest, Inc.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Python is a trademark of the Python Software Foundation.
Any other trademarks I mentioned without realising are trademarks of their respective holders.
