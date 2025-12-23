
from https://ssb22.user.srcf.net/gradint/cmaster.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/gradint/cmaster.html) just in case)

# Removing Android “Clean Master” malware

In 2019 I was asked to fix an Android 8 tablet that had advertising on its lock screen and notification area, which appeared to have been put there by an app called “Clean Master” which the user didn’t remember installing. Removing the app stopped the advertising, but a few days later the app re-appeared by itself. It was not present in Play Store’s “My Apps” page—you had to go to Settings / Apps / All to see it—and the “App Info” page said it had Camera, Location, Storage and Telephone permissions, with “Display over other apps” allowed, and said “App installed from Settings” (Version 1.2).

A simple `adb -d logcat` showed mentions of package `com.sthnsqqwel.cleanmaster` (a domain which didn’t exist), so I did `adb -d backup "-apk -obb -all"` and unpacked with Android Backup Extractor to see if I could find references to this package in any of the *other* apps. (The tablet was encrypted and made me set an encrypton key on the backup, and I was on MacOS 10.7 so as described in the `README.TXT` I had to upgrade the system `local_policy.jar` file with Oracle’s “unlimited strength” cryptography policy file, which I believe to be legal for use in the UK.) After unpacking with `tar -xvf`, everything looked in order (apart from the unwanted `com.sthnsqqwel.cleanmaster` app and a couple of unexplained mentions of a Baidu API) *but* the set of apps that had been backed up was nothing like the set of all apps we knew to be installed on the device. Clearly, some developers are setting `android:allowBackup="false"` in their `AndroidManifest.xml` files—cleanmaster itself *wasn’t* doing this, but whatever other app had surreptitiously installed it (if that’s what happened) *was* hiding itself, and I wasn’t in a position to root the device, which would in any event have destroyed the evidence along with the rest of the user’s data.

Nor could I get anywhere with `adb -d shell`, again due to permission issues (couldn’t access the directory where the apps are stored).

So I just had to run with the hypothesis that cleanmaster was *probably* being installed by a malicious payload uploaded to a rogue advertising library in use by one of the apps the user had installed, most likely one of these:
* Apple Daily (Next Mobile Limited)
* Hong Kong Toolbar (Commercial Radio Productions Ltd)
* Yahoo News Hong Kong (Yahoo)

None of these apps had been granted a permission like `INSTALL_PACKAGES`, but it’s plausible the rogue advertiser found a flaw that enables background installation of packages without permission on that particular version of Android. Since none of these apps were actually *needed* to access their publishers’ material (the web browser could do it just as well), I summarily uninstalled all three of the above as well as Clean Master.

(Some months later, the user allowed a friend’s child to install games on the tablet, and one of them left an unwanted advertising app called “omaiz” which slowed down the OS to the point of unresponsiveness. This was easily uninstalled via Settings / App manager.)

In May 2020, the “Clean Master” malware had reappeared (this time able to force-display advertisements over any app or the Settings) and the user was found to have re-installed Yahoo News Hong Kong. Therefore I now most strongly suspect that **Yahoo News has a flawed advertising mechanism** that allows “Clean Master” malware to be installed.

We will not obtain any more data from this tablet as it was physically damaged by battery swelling in the final week of May 2020.

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Android is a trademark of Google LLC.
Baidu is a trademark of Baidu Online Network Technology (Beijing) Co. Ltd.
Oracle is a registered trademark of Oracle Corporation and/or its affiliates.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
