
from https://ssb22.user.srcf.net/elec/nav.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/elec/nav.html) just in case)

# Satellite navigation devices that work with GNU/Linux or Mac

Some drivers prefer dedicated satellite-navigation devices over mobile phone ‘apps’ because the dedicated devices are less likely to fall off the dashboard during braking. But you can’t just buy the cheapest device and expect to succeed in updating it.

I gave this page a slightly misleading title because I think most people who search for “SatNav that works with Linux” or similar *really* mean “SatNav that does not require me to buy a new Microsoft Windows computer to update it” and might not have considered units that can be updated “without **any** computer”. For these you will usually require a Wi-Fi base station—or a computer configured to act as one—but won’t need to run the manufacturer’s own software on it.

However, two further things are of note:
1. Not every unit advertised as “Wi-Fi capable” really can download and install updates *without* support from a Windows machine: some of them merely use home WiFi to communicate with a Windows box which must still be present. So before purchase, double-check the manufacturer’s website for PDF manuals and/or other update advice and be sure it doesn’t instruct you to do anything “on your computer”.
   * In 2018 the only car products I could find with *self-sufficient* WiFi updates were: TomTom Go Basic, TomTom Go Essential, TomTom Go 520 Wi-Fi, TomTom Go 5200 Wi-Fi, TomTom Go 620 Wi-Fi, TomTom Go 6200 Wi-Fi, TomTom Via 53, Garmin Drive 51, Garmin Drive 5S, Garmin Drive 61, Garmin DriveSmart 51, Garmin DriveSmart 61, Garmin DriveSmart 7. Quite a few other TomTom and Garmin products could *not* do it, so *don’t* just look for brand names.
   * Try searching for “how to update without a computer” and check which model numbers the manufacturer says these instructions are for.
2. Updates are always at the manufacturer’s discretion. The shop might have a big shiny notice saying “lifetime updates”, but the small print in the manual will tell you that “lifetime” means only for however long they *provide* the updates, so it’s a meaningless circular term apparently meant to deceive customers into thinking they’ve bought support for life. (1990s floppy disk manufacturers used a similar trick with the phrase “lifetime guarantee”.) In practice the updates are likely to cease when the company feels it has to change its update servers in a way that no longer maintains compatibility with firmware on the device you bought, and/or their newest updates begin to require more memory than you have. But it’s still useful to be able to receive map updates *for a while*.

## TomTom Basic updates

Immediately after logging in to the Wi-Fi hot-spot and entering the credentials for a newly-created “TomTom account”, the device said “we are having trouble accessing TomTom services”, which turned out to be because the firmware had somehow got itself into a state that treated the Wi-Fi access point as “out of range” (even when placed just centimetres from the router). This could be worked around via power off (not sleep) and on again, but then the disconnected state repeated itself during the update. Thankfully, in our case, the update process *did* continue from where it left off after a second power-cycle: it hadn’t left the system in an unbootable inconsistent state.

The update process of course drove the ADSL to its maximum capacity and thereby increased the probability of other traffic being dropped, but it *is* possible to tell the device to send its traffic through a proxy, which can limit the rate if desired.

We also found that, if you have a mobile phone capable of acting as a Wi-Fi ‘hotspot’, and a data plan that permits it, you can have the Basic obtain realtime traffic updates via the mobile hotspot, which might be more convenient than sending them over Bluetooth from the proprietary phone ‘app’. (Traffic updates are not compulsory; the device can work entirely offline with only a GPS/GLONASS signal.)

In 2022 our TomTom Go Basic got stuck in a continuous loop of “not enough space” messages when trying to update. When we power-cycled the device and went to Menu / Maps / Delete maps, it went back to an “updating” screen (at 98%), then said we couldn’t delete the only map, then allowed us to repeat the updates.

Obviously these notes are posted in the hope that they are useful but without any warranty, so if you brick your navigation device and arrive late for a million-dollar deal or something then don’t sue me.

## Don’t rely on “speeding alerts”

The Basic device has a “speeding alert” facility but it’s off by default. If turning it on, note that:
1. it does *not* issue an audio alert until you are driving **at least 4mph over the limit** (so don’t rely on it to warn you about accidental *slight* speeding), and
2. its database has been known to hold **outdated** limits *even if you have the latest update*. For example we found a place in Cambridge which had been 20mph for 2 years but TomTom still had it on file as 30mph (and it’s unclear how to report this on TomTom’s “MapShare” service). We also found a road in Bury which they had at 30mph but was actually 50mph, which was a good place to discover how much you have to ‘speed’ before getting the audio, but the reverse (map has higher limit than road signs) is more disconcerting.

It might be better *not* to enable these alerts if there is any danger of their giving the driver a “false sense of security”—drivers should know to check the signage themselves.

A related concern is it’s **too easy to turn off sound** on this device. The ‘menu’ button appears at the bottom left of the map screen, and, once pressed, is replaced by a ‘mute’ button—making ‘mute’ rather too easy to activate by mistake and without noticing.

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Bluetooth is a registered trademark held by the Bluetooth Special Interest Group.
Garmin is a trademark of Garmin Ltd. or its subsidiaries, registered in the USA and other countries.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Mac is a trademark of Apple Inc.
MapShare is a trademark of Garmin Ltd. or its subsidiaries *and also* a trademark and brand of TomTom International B.V. (does it depend on the font?)
Microsoft is a registered trademark of Microsoft Corp.
TomTom is a trademark of TomTom International BV.
Wi-Fi is a trademark of the Wi-Fi Alliance.
Windows is a registered trademark of Microsoft Corp.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
