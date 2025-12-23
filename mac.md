
from https://ssb22.user.srcf.net/setup/mac.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/setup/mac.html) just in case)

# Mac magnification setup

OS X and macOS have built-in magnification:
* In 10.7 and below, it’s under **System Preferences / Universal Access**,
* In 10.8+ it’s System Preferences / Accessibility / Zoom, and you may also need to enable the keyboard shortcuts under System Preferences / Keyboard / Keyboard Shortcuts / Accessibility as they are no longer enabled by default (10.8 disabled the “invert colours” shortcut by default, and others were turned off around 10.11)

Rhyme for remembering the keyboard shortcuts:

The Mac does not from Windows lift

these keys, so you should **not** press *Shift*.

But press **Control**, **Command** and **Alt**,

These three, with **8**, a glare can halt.

And if the zoom be lacking whole,

then press these keys **without Control**.

For **plus** and **minus** take the same

as **8**: the **Alt** and **Option** twain.

## Setting minimum and maximum zoom

If you set Minimum Zoom to 1 (the extreme left of the slider), and Maximum Zoom to your preferred level (e.g. 2), that will allow you to switch between 1 and 2 with a single keypress. You can still zoom further by holding down the keys, but it’s useful to be able to quickly get to a preferred integer level.
* In 10.7 and below, these settings are under an “Options” button by the Zoom section of Universal Access.
* In 10.8+ click on More Options.
* In 11.x and 12.x click on “Advanced” and “Controls” but the new slider appearance makes it difficult to set to an integer.

## External monitors for laptops

When macOS 11 is running on a laptop that’s connected to an external display, it defaults to a dual-screen setup that interacts rather badly with zoom: the *magnified* image is divided over *both* screens, cannot be panned left or right unless you drag the mouse to the edge of the *corresponding* screen, and tends to split windows down the middle in a way that doesn’t work very well when the screens are different physical sizes.

The Accessibility Zoom “Choose Display” setting gives you the option of showing the zoomed image on the external display while showing the un-zoomed image on the laptop. However, **I do *not* recommend this** because:
1. it causes the display-invert option to invert only the *un*-zoomed version (although at least macOS 11+ has a “dark” theme under System Preferences / General, but not all applications make this work as well as display inversion),
2. in macOS 12 it activates a ‘bug’ that causes image “smoothing” (i.e. blurring) to be turned on regardless of the value of its checkbox,
3. it does not persist across a screen lock (so it encourages you to disable the lock, which might not be the best idea depending where you work), although settings are more likely to persist across logout or restart,
4. it does not persist across a temporary loss of power to the external monitor,
5. and it can cause a Mac kernel crash on resume from suspend, thus encouraging you to turn off energy saving, which has climate-change consequences.

Instead, you can first set “Choose Display” to “all” (the default), then go to System Preferences / Displays (not to be confused with “Display” under Accessibility), Display Settings, and set “Use as” to “mirror”, “optimise for” to internal (the drop-down might become mislabeled after this change), and resolution “scaled” for “larger text”. You can then zoom and/or invert and see the resulting image on both displays.

Using a “mirror” display has the side-effect of **muting all notifications** on macOS 12, unless a box is ticked to “allow notifications when mirroring or sharing the display” in System Preferences / Notifications. The location of this box is likely to be behind the Dock if you’re using ‘scaled for larger text’, so you’re not likely to notice it’s there unless you hide the Dock (and there doesn’t seem to be a keyboard shortcut)—too bad their interface designers had not invented some means of scrolling large dialogues.

If you close the lid of the laptop, macOS reverts to zooming a single external display, and you typically have to *re-do* all the settings, and again when you re-open the lid. It’s worse if you’ve used “Choose Display” and were zoomed in at the time the lid is opened—this can put the Mac’s graphics subsystem in an inconsistent state (e.g. desktop vertically repeated) and you’ll have to zoom out before it lets you change the settings back. Unfortunately I have not found a way to restore preferred zoom settings from a command-line script: it requires painful small-print mouse work every time. Therefore you should probably leave the laptop open at all times if you need to use its internal camera.

## Reducing anti-aliasing and smoothing “blur”

It appears that the zoomed image is processed as follows:
1. Text is anti-aliased onto a non-zoomed screen buffer
2. The pixels are then mapped onto the larger zoomed buffer (which degrades quality if the zoom factor is not an integer)
3. An additional “smoothing” step is optionally applied to the new image (I don’t know if this step has knowledge of the original pixels, but it doesn’t seem to have any knowledge of the original fonts).

The above steps acting in combination can blur the result. So my suggested settings are:
* Make your preferred zoom level an integer. That should at least stop the middle step from harming image quality.
* In the zoom options, try turning off “Smooth images”, especially if your text has been antialiased to start with.

Where possible, turn off antialiasing altogether:
* try typing `defaults write .GlobalPreferences AppleAntiAliasingThreshold 100` in a Terminal (it takes effect when you restart applications).
* In Terminal Preferences, try setting a font that has a bitmap version (e.g. Andale Mono rather than Menlo); Terminal should then let you turn off its own “Antialias text” box so you can use the bitmaps.
* If Terminal or xterm sometimes crashes, you could try alternatives like iTerm:
  * In iTerm 1 (more stable but does not support speaking selected text), set fonts and colours under View / Session info and disable session-initiated window resizing under Bookmarks / Manage profiles / Terminal
  * In iTerm 2 you have to edit the default profile in Profiles / Open Profiles to reach those settings, and *don’t* tell it to report the terminal type as `xterm-256color`—if you do, any “screen” session you enter (perhaps on another host) may activate a bug that prevents command-line wrapping for the rest of the iTerm2 session—if you want to change the reported terminal type from `xterm` so your scripts know it’s not Mac’s X11, try `xterm-color`.

## Avoiding “getting lost” in panning

In the zoom options’ screen movement section, I usually find the option called “So the pointer is at or near the center of the image” works better than the other two, *unless* you are working with tooltips, in which case set the mouse “tracking speed” (acceleration) fast so you can use the “when the pointer reaches an edge” setting for more control.

Ideally it would be possible to reduce the desktop’s overall height and width to about 1.6 to 1.8 times that of the magnified area, to reduce the chances of “getting lost”. This is [possible on non-Mac systems with old-style X11 setups](https://ssb22.user.srcf.net/setup/zoom.html) but does not seem to be available on the Mac without reducing the magnification factor to a non-integer.

If you do have to reduce the magnification factor to less than 2 and the resulting text is too small, then you might be able to make up the size by also using a lower-resolution display mode. In 10.x modes can be set under System Preferences / Display; in 11.x use System Preferences / Displays / Scaled / Larger text. (Some third-party applications are not tested with this setting and might display windows larger than the screen.)

# Speak selected text

On OS X 10.5+ you can enable a **keyboard shortcut to speak selected text** (defaults to Alt-Escape; press a second time to stop). This needs to be switched on in the text-to-speech preferences (in 11.x it’s Accessibility / Spoken Content / Speak selection).

In 10.8, you need to take two additional steps to work around a bug: (1) change the keyboard shortcut (if you like the default, change it back again), (2) press “Play” to hear the voice’s demo. The shortcut key will then work. (These additional steps were not needed in 10.5 through 10.7.)

The shortcut works in most Mac applications, including Terminal, but not iTerm 1 or (some versions of?) Chrome.
* It works in iTerm 2 at least from the 2012-12-24 release (not the stable 2011 v1.0.0 edition—that version reads the entire window instead of the selected text). However I recommend using at least the 2013-01-22 release which also fixes some crashes.
* Chrome should still work via “Speech” / “Start speaking” from the context menu, but Alt-Escape might not work as it does in Safari.
  * If Safari is slow, try regularly removing its cache files from `Library/Caches/Safari` or `Library/Caches/com.apple.Safari` (using the Terminal or a script, *not* from Safari’s menus)—it seems some versions of Safari mistakenly let these files accumulate enough to slow it down

Here is a [script to change the voice from the command line](macvoices.txt) (useful if you work in several languages).

# “Linuxify” the Mac command line

Here is a [script to make the Mac more GNU/Linux-like](https://ssb22.user.srcf.net/setup/maclinux.txt) by:
* Assigning all Mac applications to shell commands whenever possible
* Providing functions for `wget`, `watch`, `umount`, `halt` etc when these commands are not available

The script can be added to, or sourced from, your `~/.zshrc` on 10.15+, or your `~/.bashrc` and `~/.bash_profile` on earlier versions (it’s written in a common subset of `bash` and `zsh`).

You may also want my [Emacs configuration](https://ssb22.user.srcf.net/setup/emacs.html).

# Using Old Safari “Reader” with zoom

[Historical interest only: please do not use old versions of Safari on untrusted websites. It doesn’t work with modern versions of HTTPS anyway.]

The “Reader” feature of Safari 5.0, 5.1 and 6.0 doesn’t work well with zoom because it uses a fixed-width layout which can easily be too wide for the zoomed viewport; this was fixed in 6.1 but if you’re stuck with an old version you can try this [reader narrowing script](narrow-reader.sh) (requires administrator access to the machine) which also allows you to change the colours.

Safari 6.1’s Reader fixed the width issue but doesn’t allow colour changing (unless you invert the whole display in Universal Access); it doesn’t respond to my [stylesheets for low vision](https://ssb22.user.srcf.net/css/) or to the above script.

# Mac screen sharing with magnification

OS X has included VNC “screen sharing” since 10.4, but 10.7 introduced a feature that can make it hard for non-Mac VNC clients if your desktop size is not 1280x1024.
* When a non-Mac VNC client connects, it is presented with a login screen. (Mac clients can use a proprietary protocol extension to bypass this screen.) This login screen measures 1280x1024.
* When you get through to the desktop, if the desktop dimensions are different (for example because you left a session running with different dimensions) then the VNC dimensions will be changed mid-session, which may crash your VNC client.
* You could make sure to log out before connecting to VNC, but then you’re “stuck” with a 1280x1024 desktop size; any attempt to change this in Display Preferences can crash the client again.

One solution is to use an alternative VNC server, such as Vine (OSXVnc) which can be set to serve just one user session (can run on login with automatic login). Notes:
* Some versions of OSXVnc severely corrupt the display if your horizontal desktop resolution is not a multiple of 8. So if your monitor has an odd resolution like 1366x768, try setting the desktop to 1360x768 or to a lower multiple-of-8 resolution.
* If the Mac boots without a physical display attached to it, it might not “remember” that display’s resolution (and if the resolution is unusual then it might not even be listed in Display Preferences) so you may have to settle for different dimensions in this situation.
* For keyboard layouts, it seems to work best to set your preferred layout at the VNC *client*, and leave both Vine Server and Mac’s “Language & Text” set to “US”. You might still find the Command and Option keys are switched around.
* **Zoom does not work over VNC**.
  * If you can [reduce your X11 resolution](https://ssb22.user.srcf.net/setup/zoom.html) on the client side then you should be able to pan around the desktop even if your X server does not support panning (just set one low resolution and let TightVNC do the panning, perhaps putting nothing but the `vncviewer -fullscreen` command in your `.xsession`, but it’s faster if your X server has full virtual desktop support). If however your low-resolution mode is blurred then the magnified desktop will be blurred.
  * Alternatively you could try running the viewer within a suitably-sized X-based VNC server and perform [software VNC magnification](https://ssb22.user.srcf.net/setup/vnc-magnification.html), but this is slow unless you have a sufficiently capable client. (Don’t try doing that part of the processing on the Mac side—the protocol overheads introduced by x11vnc magnification will slow it down even on a local LAN.)
* Bizarre bugs can crop up such as some text in XQuartz/WINE windows not being displayed on the VNC client unless the text is selected. Sometimes moving the affected window can help, but not always. (You could however use the normal X11 protocol over SSH if you are only using X applications.)

Fundamentally it’s still best to use a Mac desktop by connecting the display directly to the machine.

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Apple is a trademark of Apple Inc.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Mac is a trademark of Apple Inc.
Safari is a registered trademark of Apple Inc.
VNC is a registered trademark of RealVNC Limited.
Windows is a registered trademark of Microsoft Corp.
Zoom is a trademark of Zoom Video Communications, Inc.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
