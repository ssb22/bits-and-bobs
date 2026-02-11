# bits-and-bobs
Miscellaneous scripts etc from https://ssb22.user.srcf.net
(also [mirrored on GitLab Pages](https://ssb22.gitlab.io/) just in case)

* [ap-setup](ap-setup.sh): set up a Wi-Fi access point on a Raspberry Pi Zero W
* [ballgame](ballgame.py) and [helper](helper.py): see [Introducing OOP in Python games](oop.md)
* [brl2unicode](brl2unicode.py): translate ASCII Braille to Unicode Braille
* [cd-clean](cd-clean.py): cleans up filenames from GraceNote database etc., e.g. for migrating from Mac iTunes to GNU/Linux MiniDLNA (used in [our collection](cds.md); see also [Alexa skills notes](spotify.md))
* [CD padder](cdrdao.py): see [spaced-out audio tracks with cdrdao](cdrdao.md)
* [chat-save](chat-save-js/): pastable Javascript for exporting chat history from various browser-based platforms
* [dv2qw](dv2qw): use Yubikey etc without coming out of Dvorak layout
* [dvpty](dvpty.py): use Dvorak when SSH'ing from public library etc
* [flatplan](flatplan.py): draw an SVG diagram of a flat from perimeter measurements
* [FreeBSD setup script](freebsd-setup.sh) for low vision tested on Mac VirtualBox with screen magnification
* [gemini-tts](gemini-tts.py): calls Gemini's text-to-speech API
* [get-python2](get-python2.sh): set up old python2 for testing
* [git2gmi](git2gmi.py): summarise recent history from multiple GitHub projects as Gemini Protocol markup
* [gitify](gitify.sh): create commits from file timestamps
* [log-alert](log-alert.py): checks Apache logs for people doing too much
* [logfit](logfit.py): fit log-plot to points
* [macvoices](macvoices.txt): change Mac system voice and language from the command line (see [Mac magnification setup notes](mac.md))
* [malware blocking nginx configuration](malblock-nginx.conf) (no longer works on Chrome 140 which bypasses the proxy's DNS) see [anatomy of a shady advertising network](shady.md)
* [narrow-reader](narrow-reader.sh): make Safari 6's "Reader" mode narrower for use with magnification (no longer works on current Macs)
* [nextbin](nextbin.py): briefly query Cambridge bin collection dates for a preset address on your Amazon Alexa devices (developer setup required) or command line
* [nextbus](nextbus.py): briefly query NextBuses.mobi for a preset nearest stop on your Amazon Alexa devices (developer setup required) or command line
* [offline-updater](offline-updater.py): see [offline package installation for Debian-based GNU/Linux distributions](offline-updater.md)
* [oil](oil.py): plot simulations for oil-filled radiators on my [heating a flat discussion](oil.md)
* [openid-cli](openid-cli.py): run OpenID with terminal-based authentication (see [documentation](openid-cli.md))
* [pbmtobbc](pbmtobbc.py): convert PBM bitmaps to BBC Micro VDU codes
* [repo-setup](repo-setup.sh): clone Git repository with mulitple push URLs
* [ssh-android](ssh-android.sh): expect script for SSH'ing over an Android 4.4 device (see [desktop SSH via Android devices](ssh-android.md))
* [telegram-backport](telegram-backport.py), [telegram-old-restore](telegram-old-restore.py): save/restore Telegram messages in the format of older versions
* [texdate](texdate.py): add file's timestamp as a LaTeX `\date` to old letters
* [tg-setup](tg-setup.sh): telegram-cli setup script for gcc 14
* [tsv-padmax](tsv-padmax.py): pad TSV data for GitHub's display

## Other notes in this repository
* [Adding Chinese web pages to Baidu](baidu.md)
* [Bolo Adventures “walk-through”](bolo.md)
* [Cambridge to London avoiding large stations](london.md)
* [Cat scarers becoming audible](cat.md)
* [Chess FEN codes for handicapped games](fen.md)
* [Civica UK is wrong about middle names](midname.md)
* [Upgrading old Windows to GNU/Linux](linux.md)
* [Converting “1000 imp/kWh” to watts](imp.md)
* [Current-transformer “energy monitors”](ct.md)
* [Eating at other Cambridge colleges](buttery.md)
* [Eulerian paths around polygons](eulerian.md)
* [HIFU and Sonata on the NHS](hifu.md)
* [How NOT to marry a foreign national](visa.md)
* [How to use Economy 7 effectively](e7.md)
* [Instructions for “F95B” portable rechargeable fan](f95b.md)
* [“Legal name fraud” nothing to worry about](badname.md)
* [Magnetic field physics: is your phone charger really killing you?](sleep.md)
* [Manually removing Windows “adware” with race conditions](rising.md)
* [Openreach broadband providers](openreach.md)
* [Pen-sized digital voice recorders](dvr.md)
* [Removing Android “Clean Master” malware](cmaster.md)
* [Satellite navigation devices that work with GNU/Linux or Mac](nav.md)
* [Shower-head water filter tested](shead.md)
* [Solving Micropower Chess (1982)](bchess.md)
* [The Telegram Borrowers](borrowers.md)
* [Toothpastes suitable for an electric brush](toothpaste.md)
* [UK citizenship application and referee requirements](citizenref.md)
* [UK passport application questions](passport.md)
* [Using Microsoft Windows with low vision](windows.md)
* [Why I don’t mind training “AI”](aitrain.md)
* [Why I unsubscribe from MailChimp](mailchimp.md)
* [Why Wi-Fi routers should be left switched on](router.md)
