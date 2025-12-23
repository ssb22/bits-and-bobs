
from https://ssb22.user.srcf.net/setup/linux.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/setup/linux.html) just in case)

## Upgrading old Windows to GNU/Linux

As a small public service to the numerous non-technical users of ageing equipment I’ve met, from 2014 to 2025 my website included a piece of Javascript which displayed the following message at the top of all my pages if it detected an outdated version of Windows. I removed this script in 2025 due to (1) inability for a website to distinguish between Windows 10 and Windows 11 due to new anti “fingerprinting” browser constraints and (2) Google using new secret site-quality algorithms that were downgrading my site for an unknown reason which might possibly have been too much Javascript mentioning old versions of Windows (how am I supposed to know?—but if the fingerprinting restrictions now make the script less likely to work anyway it makes sense to remove it if in doubt), however the warning is very much still correct:

# Connecting old Windows to the Internet is dangerous. Upgrade to Linux urgently!

My site detected you’re using **an old Windows computer**, and I’m worried about your safety. [Microsoft’s security blog](http://web.archive.org/web/20131028235030/http://blogs.technet.com/b/security/archive/2013/08/15/the-risk-of-running-windows-xp-after-support-ends.aspx) said:

> When Microsoft releases a security update...criminals will...identify the specific section of code that contains the vulnerability...develop code that will allow them to exploit it on systems that do not have the security update installed on them. They also try to identify whether the vulnerability exists in other products...if a vulnerability is addressed in one version of Windows, researchers investigate whether other versions of Windows have the same vulnerability...the Microsoft Security Response Center...[releases] security updates for all affected products simultaneously... **But after April 8, 2014, organizations that continue to run Windows XP won’t have this advantage over attackers any longer. The very first month that Microsoft releases security updates for supported versions of Windows, attackers will reverse engineer those updates, find the vulnerabilities and test Windows XP to see if it shares those vulnerabilities. If it does, attackers will attempt to develop exploit code that can take advantage of those vulnerabilities on Windows XP. Since a security update will never become available for Windows XP to address these vulnerabilities, Windows XP will essentially have a “zero day” vulnerability forever.**

This also applies to Windows Vista (ended in 2017), to Windows 8 (8.0 ended 2016 and 8.1 ended 2023), to Windows 7 (ended 2023, extended from 2020), and to Windows 2000 and earlier.

## What does this mean?

Attackers typically scan across the whole Internet to find computers they can attack. **Being ‘insignificant’ does NOT mean you’ll escape.** Simply connecting your computer to the Internet will be enough for them to break in and:
* Steal your bank details
* Steal your contact list, sending malicious material to your friends in *your* name
* Use your computer as a springboard to attack another target or conduct other criminal activity, potentially getting *you* blamed for it

## What can I do?

My suggestion is **GNU/Linux**, specifically a “beginner-friendly” Ubuntu-derived version.

If your computer is 64-bit capable and can boot from multi-gigabyte media (DVD or USB, not CD-only), then I suggest [Lubuntu’s LTS release](https://lubuntu.me/downloads/).
* **Back up all your documents before you try migrating your computer to Linux.**   You can do this while trying Linux *without* installing, but remember it’s slow when not using your hard disk.
* If you don’t have a DVD, you can [try “UNetbootin” to set up a USB stick](rising.md), or borrow a USB DVD reader.
* If, after installing, a laptop fails to activate its graphical display, try logging in on a console (Ctrl-Alt-F2), do `sudo apt install gdm3 lightdm`, and select `lightdm` as the active display manager. For auto-login, create `/etc/lightdm/lightdm.conf` with:

  `[SeatDefaults]

  autologin-user=` (your user name)

  `autologin-user-timeout=0

  user-session=Lubuntu`

  You may now remove the `sddm` package.
* If the display is stuck on 640x480 resolution, from a terminal (or console) type `sudo nano /etc/default/grub` and uncomment `GRUB_TERMINAL=console` (after saving you will then need to type `sudo update-grub` in the terminal).
* You can run some legacy Windows programs using WINE (use `sudo apt install wine`; some Chinese applications additionally require `fonts-wqy-microhei`), and you can also install `hunspell-en-gb` for British spelling in LibreOffice (you might later need to purge all `libreoffice` packages and reinstall if text does not appear on printouts and PDF files). Most other “standard” applications (Firefox etc) are pre-installed, although you might like to browse Ubuntu’s package lists to see if there’s anything else you’d like (e.g. `thonny` for learning to program: Thonny 4 contains a pro-Ukraine message that might get you in trouble in some countries, but Ubuntu 22.04 LTS still uses Thonny 3.3).
* You may also want `sudo apt install swapspace` if you didn’t create a swap partition from the installer and don’t have much RAM.
* For Chinese pinyin input, `sudo apt install ibus-pinyin` (add Cangjie via `ibus-cangjie` and its HK variant `ibus-table-quick`), put `run_im ibus` into `.xinputrc` (or run `im-config` to do it), and set Preferences / LXQt settings / Session Settings / Autostart / Add / Command `sh -c "while true; do ibus-daemon -rx; sleep 1; done"` (and run Preferences / IBus Preferences to add input methods)

### What about even older computers?

Most ‘consumer’ PCs sold since early 2007 (when Vista was new) can read DVDs and run 64-bit code. If your computer is older than that (e.g. Windows XP era) then I suggest using the old [wattOS-LXDE R9 CD-ROM image](https://web.archive.org/web/20170325011354/http://www.greygamer.com/iso/wattOS-R9-32.iso) and upgrading after installation. It also works from USB via UNetbootin etc.
* On old Pentium M machines you might need the `forcepae` boot option. On newer machines you might need to disable “Secure boot” in the BIOS.
* If WiFi doesn’t work, try Preferences / Additional Drivers and see what package it needs. If you don’t have a wired Internet connection to install these, you’ll have to open a Terminal and do `apt-get -y --print-uris bcmwl-kernel-source` or similar, possibly correct the resulting URLs (e.g. `linux-libc-dev` is now in the security updates section of Ubuntu 14.04) and bring them on storage media.
* If the @ and `"` keys are swapped (and if this bothers the user), try `sudo dpkg-reconfigure keyboard-configuration`
* Upgrade is recommended for online use: R9 was based on Ubuntu 14.04 which lost support from the security team in 2019; it can be upgraded to 16.04 (which was supported until April 2021), and from there to 18.04 (which was supported until May 2023) although 18.04 did drop some early “586” CPUs like the Cyrix III that may have ran Windows XP. Unsupported GNU/Linux versions are not ideal, but they’re still more secure than the unsupported Windows versions they replace.
  1. As root, type `do-release-upgrade` to reach 16.04
  2. `apt-get install lxsession-logout linux-generic-hwe-16.04` to avoid 16.04’s “hung shutdown” bug associated with kernel version 4.4.0
  3. Type `do-release-upgrade` again to reach 18.04, in which case you might also need `apt-get remove resolvconf`
* Some users might also want `brasero` for writing CDs, `wine` for running legacy Windows applications, and `libreoffice` (if it crashes try turning off Java in its Preferences, and install `myspell-en-gb` for British spelling). Also `vlc` for playing videos (and doing this from inside Firefox may require `ubuntu-restricted-extras`; on 16.04 you can also try `libdvd-pkg` for playing commercial DVDs).
* For Chinese fonts, `sudo apt-get install fonts-wqy-microhei`; pinyin input can be added as above (although the LXQt setting is not needed on R9, 16.04 or 18.04), or for limited single-character handwriting input, `sudo apt-get install tegaki-recognize tegaki-zinnia-simplified-chinese` and add it as an icon on the application launcher
  * **LaTeX users beware:** Do not install the `texlive-full` package if the user is likely to paste Traditional Chinese into LibreOffice. When such pastes occur, LibreOffice looks for the first Chinese font listed, which will be Arphic Simplified if TexLive installed that under ‘A’—but the system fails to select the matching Arphic Traditional font for characters not present in Simplified, instead rendering these in a *non-matching* font which uglifies printouts. So if you do leave TeXLive on the machine, I suggest uninstalling its Arphic fonts if the user won’t be coding for old-style CJK-LaTeX. (If they *will* use CJK-LaTeX *and* paste Traditional Chinese into LibreOffice then you might just have to tell them to correct LibreOffice’s font choice after every paste.)
* Developers: if you have a 64-bit CPU and want to compile for it (or if you want to run Zoom, which started to require 64-bit after version 5.4), try:

  `dpkg --add-architecture amd64

   apt-get update

   apt-get install linux-image-generic:amd64

   reboot

   apt-get install gcc:amd64 cpp:amd64 gdb:amd64`

  If you’ve upgraded to 16.04, you will likely also need `linux-generic-hwe-16.04:amd64 gcc:amd64 cpp:amd64 gcc-5:amd64 cpp-5:amd64 binutils:amd64 g++:amd64 g++-5:amd64 lxrandr:amd64 x11-xserver-utils:amd64` which in 16.04 is somehow incompatible with `libtool` (frequently required by `autogen.sh` files in source packages) so you might need temporarily to switch back to a 32-bit-only compilation environment in those circumstances, or use conan.io etc instead of autogen.
  * If you’ve upgraded to 18.04, you might see an error message from `iucode_tool` updating `initramfs`—this does *not* mean your system is unbootable. The system should still boot without the microcode updater, and it can be restored when the initramfs is updated after next boot.

  To upgrade the *entire system* to 64-bit, by far the easiest way is a fresh install: the Lubuntu 20.04 installer (which requires 64-bit) has an option to resize your existing partition and install alongside, which might help with the migration (but backup anyway just in case). The move from LXDE to LXQt may require some manual setup.

## What if I don’t want to install GNU/Linux?

Well there is another alternative system called BSD (a version called “GhostBSD” is fairly beginner-friendly), but if you don’t want to leave Windows *at all* then you will likely need a **new computer** if you wish to continue to use the Internet. Your old computer can perhaps be put to good use by someone who doesn’t use the Internet, or by a trustworthy GNU/Linux expert (I say ‘trustworthy’ because they can sometimes recover confidential things you thought you’d deleted). For new equipment, I suggest a Raspberry Pi 500 (or 400) which comes with GNU/Linux preinstalled; you might need something more substantial, but it should still be possible to avoid Windows.

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
CJK was a registered trademark of The Research Libraries Group, Inc. and subsequently OCLC, but I believe the trademark has expired.
Firefox is a registered trademark of The Mozilla Foundation.
Google is a trademark of Google LLC.
Java is a registered trademark of Oracle Corporation in the US and possibly other countries.
Javascript is a trademark of Oracle Corporation in the US.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Microsoft is a registered trademark of Microsoft Corp.
Raspberry Pi is a trademark of the Raspberry Pi Foundation.
TeX is a trademark of the American Mathematical Society.
Wi-Fi is a trademark of the Wi-Fi Alliance.
Windows is a registered trademark of Microsoft Corp.
Zoom is a trademark of Zoom Video Communications, Inc.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
