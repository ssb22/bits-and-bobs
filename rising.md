
from https://ssb22.user.srcf.net/gradint/rising.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/gradint/rising.html) just in case)

# Manually removing Windows “adware” with race conditions

Every so often I am asked by a local Chinese family to “fix” an old Windows computer that is displaying unwanted Chinese-language advertisements. Usually one family member has used the computer for games or other entertainment that installed the advertiser’s software, and other family members are annoyed by it. I hope the advertisers won’t hold a grudge against me for posting removal instructions—it’s actually better for their reputation if the instructions exist. (Perhaps they already exist somewhere in Chinese but my Chinese skills weren’t good enough to find them.)

The best “removal” is to [replace Windows with a good installation of GNU/Linux](linux.md) or similar, but I’m usually asked not to do that. The off-the-shelf “adware removal” products of the English-speaking world are rarely helpful; I don’t know if other Chinese products would help, but it’s usually possible to do it manually as follows.

While well-behaved Windows programs usually have working uninstallers, advertisement software is usually *designed to be difficult* to remove. In *some* cases you can remove things as follows:
1. Enter “Safe mode” (F8 or Fn-F8 on boot)
2. Search the registry for offending registry names e.g. `Babylon`, `BrowserDefender`, `BitGuard`, `PerformerSoft PC Performer` (I’m listing these because I have seen malware operating under those names; no offense meant to any bona-fide software that shares a name with it)
3. Check all startup folders and the registry. In the registry, remember to check:
   * **All** of the `Run`-like sections under Software / Microsoft / Windows / CurrentVersion, in both HKLM and HKCU (many people know about these); check for `Load` sections also
   * The scheduler tasks (HKLM / Software / Microsoft / Windows NT / CurrentVersion / Schedule / TaskCache / Tasks)—not so many people know about this (also check under CurrentVersion / Explorer / SharedTaskScheduler)
   * Services (HKLM / System / CurrentControlSet / Services)
   * Winlogon settings (check HKLM / Software / Microsoft / Windows NT / CurrentVersion / Winlogon / Notify, make sure nothing has been added to Userinit.exe in Winlogon / Userinit, and check the Winlogon Shell keys in both HKLM and HKCU)
   * Windows Explorer add-ons under CurrentVersion / Policies / Explorer / Run (both HKLM and HKCU)
   * The settings of whatever Web browser is in use
4. Remember to also check for old-fashioned autoexec, autostart and INI files, and watch out for malware that replaces your folders with EXEs disguised with folder icons

but sometimes “Safe mode” is unavailable or this approach is otherwise compromised.

If you are able to reboot into a GNU/Linux or other rescue system that has reliable read/write access to the filesystem then you can often simply remove the errant files (the list of running programs in Task Manager, invoked by pressing Ctrl-Shift-Escape, might help to identify them before the reboot as long as Task Manager itself has not been tampered with), but if rebooting to a rescue environment is not an option then deleting the files might not be possible as Windows (unlike GNU/Linux etc) does not allow deletions of programs that are still running. You could try to stop them from the Task Manager, but some might have “tricks” such as running several processes that automatically restart each other whenever one is terminated, and/or having a process run as a Windows system service set to restart on any failure. An example of a self-restarting service is `RsMgrSvc.exe`, allegedly by an anti-virus company called Rising (瑞星 Ruìxīng) but one version of it launches persistent desktop tray advertisements and apparently has no uninstaller.

You could attempt to remove a program’s method of “hooking in” to the system at startup (usually via the registry, although not always in the well-known `Run` sections—there’s a host of *other* places in the registry where startup programs can hide, some of which are listed above; you could try searching the registry for the executable’s name, but note that any finds in `MSConfig` merely indicate a previous failed attempt at removal using the msconfig tool). Any registry changes you make are likely to fail with aggressive software that monitors the registry for changes, undoing what you did; sometimes you can see the undo has taken place by pressing F5 to refresh the registry view after removing something.

Sometimes the only way to fix a running system, if rebooting into a suitable rescue system is not an option, is to **exploit a race condition** in the aggressive software’s defence mechanisms. The easiest one to exploit is usually the very short delay before a process restarts itself after Task Manager has terminated it. If you manage to delete its program file in that brief moment, it will not restart (until some other process downloads it again—advertising that automatically re-downloads its missing parts is possible, so it can help to disconnect the network while working on this). After deleting all the files you can without terminating the processes, you can select the remaining files for deletion, then terminate whatever process is interfering, then quickly switch back and finish the delete before that process is re-launched. It might take several attempts for this to work, as it depends on the timing.

## Rescue system

If you *are* able to boot into a GNU/Linux (or other) rescue system that is able to gain read/write access to the Windows system files, then removing unwanted programs can be considerably easier.
* There are small, NTFS-capable distributions of GNU/Linux that can easily fit in the spare space of most USB “sticks” that are carried around for other purposes, to save you from having to carry an extra item if you never know when you might need it.
* Try “UNetbootin” to set up the USB stick from within GNU/Linux, Mac or Windows.
  * If you already have access to a machine running a recent version of Ubuntu GNU/Linux, please *do not* attempt to use `usb-creator-kde` or `usb-creator-gtk` instead: it may try to block-copy an ISO9660 filesystem to the USB, which does not always result in it being bootable on older machines. UNetbootin might require a static binary download if you can’t get a working package.
  * Although UNetbootin *can* work from an offline ISO file, at least some versions refuse to start without a working Internet connection.
  * However, if all you want is to copy files from one existing bootable USB disk to another, then all you need to make sure of is that the generic Syslinux MBR is reinstalled and the partition is bootable. This MBR is the **first 440 bytes** of the device, and is also supplied as `mbr.bin` in Syslinux and UNetbootin; you can install it on GNU/Linux or Mac systems with `dd conv=notrunc bs=440 count=1` (supplying `if=` and `of=` as appropriate, likely `/dev/sd`... for Linux and `/dev/disk`... for Mac) and set it bootable with `fdisk`.
* Many computers can boot from USB if you press a certain key during startup: try Escape or F9 or F12. If the USB device is not recognised in one port, try another port, as it appears some older machines will boot only from the first host controller.

The obstacles are usually:
1. **NTFS won’t mount rw**: try explicitly using `mount -t ntfs` (or a desktop icon) instead of just `mount` or `ntfsmount`
2. **Rescue system is too old**—if it dates from some time ago (been in a pocket for years) then it may have issues with Chinese filenames. UNetbootin should be able to update it if it’s on USB.

## Disclaimer

I hope the above pointers are useful, but I am not legally responsible for any consequences. (If you do manage to completely “trash” the system, may I suggest choosing something other than Windows next time, or if you do re-install Windows then at least warn all users about the dangers of indiscriminate downloading.)

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Mac is a trademark of Apple Inc.
Microsoft is a registered trademark of Microsoft Corp.
Windows is a registered trademark of Microsoft Corp.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
