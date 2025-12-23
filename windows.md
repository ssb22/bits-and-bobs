
from https://ssb22.user.srcf.net/setup/windows.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/setup/windows.html) just in case)

# Using Microsoft Windows with low vision

The following notes are intended for those not in a position to [upgrade to GNU/Linux](linux.md).

Windows 7 and up have bundled full-screen magnifiers (with optional invert colours as an alternative to the Alt-Shift-PrintScreen high-contrast mode); this magnifier is available by pressing **Start-key +** (and Start-key - to reduce). The magnified text can look very blurry on some systems, but it’s not so bad in Windows 10 with the May 2020 update (which also added TTS options to the magnifier, but you may or may not be allowed to use sound if you’re on a public library computer or similar).

## Older notes

The following techniques worked for me on a Windows XP Pro laptop I was loaned by a company to do some work for them in 2007/08:
* Use one of my [low-vision stylesheets](https://ssb22.user.srcf.net/css/) for Internet Explorer. These tend to work better than the high-contrast mode you can obtain by pressing Alt-Shift-PrintScreen, and IE is used as a component in many places so set this up even if you use Firefox etc.
  * Here’s a [dark background registry snippet](https://ssb22.user.srcf.net/setup/dark-background.reg) in case you need a quick setup of non-browser colours without going through the dialogues. (Might require reboot or logout.)
* Display properties (right-click on desktop) > Settings decrease the screen resolution, and in Advanced increase the DPI (perhaps double it). This should put almost everything, including dialogue boxes, into large print. (In Vista, the DPI setting is on the left of the main display-properties panel, not under Advanced.)
* The downside of doing that is, dialogue boxes are sometimes too large for the screen, and there is often no way to pan the screen to see the rest of the dialogue.
  * Some programmers add scroll bars (although most don’t think of that)
  * It *might* be possible to press Alt-Space, select Move, and move it off the top of the screen so as to see the bottom, but only if you use the arrow keys without touching the mouse, and you cannot interact with it in this state (you have to remember what it looks like and then interact with it off-screen).
  * Sometimes you can temporarily increase the resolution and strain your eyes for a while, but Windows often says that needs a restart, unless you have told it not to in the video driver setup (which option depends on the video card; you have to look at them and find it).
  * On English Windows only, in desperate situations you can also try Start > Programs > Accessories > Accessibility > Narrator (it may also work to hold down the Windows logo key while pressing U), and navigate the dialogue box aurally, provided the programmer has not made it impossible to do keyboard navigation. Narrator is *not* a good screen reader, but it can be useful for those “you must accept the license agreement” boxes where the “accept” button is off-screen.
  * You can also remember how many times to press certain keys. For example, **to set Notepad to save in UTF-8** do Save As, type filename, press **Tab 4 times and U 3 times** and press Enter. (It’s better if you can set up [Emacs](https://ssb22.user.srcf.net/setup/emacs.html) though.)
* You will probably be maximising most of your windows and using Alt-Tab to switch between them, which can get tedious when there are many. Try using the GPL program *Virtual Dimension* from virt-dimension.sourceforge.net which allows you to set up virtual desktops with customised hotkeys (such as Ctrl+Alt+some letter), for faster switching to and from specific applications or groups of windows. (**Warning:** Recent reports suggest SourceForge has a new policy of taking over inactive Windows projects and adding advertisements or other unwanted extras to their installers. **I have not re-checked the Virtual Dimension installer for malware.** The best thing is **don’t use Windows**; try GNU/Linux instead.)
* You can set a large mouse pointer in the control panel. (And usual techniques apply, e.g. when you lose track of the pointer, whisk it toward the top left corner and watch for it there.)
* You can auto-hide the taskbar for extra screen real-estate. (Right-click on it and go to Properties.)
* Remember you can set the start menu to “Classic” and customise it to put only your own frequently-used applications at top level (drag onto Start button to add, right-click to access a menu that lets you delete). This is more reliable than using desktop icons, which often get moved around (sometimes off-screen). You probably won’t be able to navigate XP’s entire start menu hierarchy due to menus going off-screen; the best way to sort it out is in Windows Explorer or other file manager.
* The *PuTTY* SSH client can be configured to use [a small number of rows and columns](https://ssb22.user.srcf.net/setup/terminal.html), and to change the size of the font when resized or maximised. On *some* Windows setups this is also true of command windows, which allows large-print Cygwin consoles (try pressing Alt-space P and see if it will let you set a large TrueType font and smaller dimensions).

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Firefox is a registered trademark of The Mozilla Foundation.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Microsoft is a registered trademark of Microsoft Corp.
SourceForge is a trademark of VA Software Corporation.
TrueType is a trademark of Apple Inc., registered in the United States and other countries.
Windows is a registered trademark of Microsoft Corp.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
