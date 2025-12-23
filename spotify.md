
from https://ssb22.user.srcf.net/law/spotify.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/law/spotify.html) just in case)

# Spotify’s numerous “radio” channels

Before the COVID-19 pandemic I was given an Amazon Echo Dot 3 as a prize for a presentation I did. This is a “thin client” device, running a variant of Amazon’s “Fire OS” fork of Android that is not user programmable: it listens for its “wake word” and uploads audio to Amazon servers for processing there. (You might want to mute it before having any really private conversations, because it has been known to start recording by mistake and to leak snippets of your home’s audio to Amazon’s QA staff.) The unit has speech synthesis and sound playing facilities, but all interactions are driven by Amazon’s remote servers, which means all services are subject to change without notice.

The service was able to set timers and alarms, and answer questions about summary weather forecasts, sunset times, word definitions (Alexa used the Collins English Dictionary for this), city and country distance / population / time, calculator answers etc. It also provided a facility to place voice calls to other Amazon devices once these were added as contacts, although the software sometimes gets itself into a failure mode where the “call” command is acknowledged but does nothing—power-cycling your devices may be needed when this happens. It used to provide email access too, but this was removed, so I doubted that the service to place voice calls to non-Amazon phone numbers in some countries—which obviously costs Amazon—would be provided for long.

Third-party functionality was available by selecting from what Amazon called “skills” which have to be “enabled” on your account. For example you could enable BBC Sounds and use it to listen to live or catch-up radio, if you remember to start your request with the words “ask BBC Sounds to play” so it doesn’t go to the default track-request skill instead, which is either Amazon Music or Spotify. (You can also set a “routine” to catch a specific phrase and rewrite it to another.) Some ‘skills’ were not available unless you opened your Amazon account in a particular language, for example Radio Swiss Classic could not be enabled unless you had your account set to German (even though you weren’t expected to interact with it once it was playing), and some small developers even set their English-language ‘skills’ to be available only in America and not Britain (presumably by writing `en-US` instead of `en` somewhere).
* We were able to listen to Radio Swiss Classic in the UK by using the “University” skill blueprint at `blueprints.amazon.co.uk` and setting it to fetch “lectures” from the France `m3u` URL on `stream.srg-ssr.ch` (using `https`)—it has to be called something generic like “Swiss classical music” to avoid tripping the trademarks filter even if you’re not publishing this templated ‘skill’ (but again a “routine” can redirect any use of another phrase).

Developing a ‘skill’ yourself essentially involves implementing and registering a server-side API which Amazon steers you towards hosting on AWS and gives a free tier—there’s a couple in my `bits-and-bobs` Git repository for scraping next buses and running instructive Python.

We were able to set up a skill called “Our Jukebox” to play from a local MiniDLNA server to access [our CDs](cds.md)—this needed playlists to be created, and the resulting commands were quite long so we created aliases via simple “routines” (i.e. when a shorter command is spoken, the longer one is executed). But we did run into one problem with “Our Jukebox” waking us up in the middle of the night with a spoken error message many hours after use (this seems to be made less likely by making sure to go back to radio after any CD). We were not able to get any of the other available “play audio from an arbitrary URL” skills to work in practice (Sonos can do it in its default API but not Echo).

When I first got the device, it was also possible to ask Spotify to play a particular piece of music and it would play it. But this functionality did not last. Soon, Spotify was interpreting all requests for a piece of music as a request for a virtual radio station I’d never heard of, with a name very similar to the piece of music I’d asked for but which was usually playing something else in the same general genre. At first I thought this was some third-party bad actor trying the equivalent of ‘typo squatting’ by registering their “radio stations” under the names of pieces of music, so you couldn’t ask for the piece without getting the station, and I tried to work around it by asking for obscure early-music recordings but it seemed the “radio station” people had hijacked even those. However, when I carefully read the description of the Spotify “skill” and translated their marketing language back into normal English, it became clear that, whereas previously you could ask for a specific piece of music without charge but might occasionally be required to listen to an advertisement, it was now the case that you had to pay extra for the privilege of being able to ask for a specific piece of music, and if your account was not paid up then Spotify would generate a “radio station” to play something in (what Spotify thinks is) the same genre but not exactly what you’d asked for. It’s possible that Spotify gave us a trial run of the exact request service and the trial expired, or perhaps Spotify’s business model changed; it was not clearly explained. (At least the Amazon Music service did explain that specific requests now required payment.)

Spotify’s “radio” algorithm seemed to be going out of its way to be indirect: even when I asked it for *anything* conducted by Christopher Hogwood (thinking I’d at least get period performances), it played three random tracks from non-period performances of Bach, Purcell and Handel, then some ‘mood’ music (I think it confused Scott Ross the harpsichordist with Scott Ross the modern composer), then a bit of Biber, then three advertisements (one of which was for gambling) and a repeat of the same Bach track before finally playing part of an overture that really *was* conducted by Hogwood, after segueing into a movement of Telemann and then back to the Bach (it managed to pick a different track this time) then a modern improvised prelude from a Carl Friedrich Abel CD and a chorus from a non-period performance of Purcell’s King Arthur. If you want any more control than that then you’ll need an extra subscription. This of course makes the basic service completely unsuitable for those “don’t you know that piece? let me play you that piece” conversations.

On the other hand, the specific-request service that we’d previously been given didn’t always work either—it was liable to do things like play the Mozart Requiem if asked for a specific Mozart concerto. (Sometimes I miss the 20<sup>th</sup>-century search systems that could say “no, we haven’t got that” instead of pretending you’d asked for something else.)

## Using Bluetooth instead

The Echo Dot can be used as a Bluetooth speaker to play audio from another device, which then needs to be controlled separately—but sending sound output to the Echo might still be useful if that other device’s loudspeaker is not as good as the Echo’s (the Dot 3’s is quite reasonable, although I can’t say as much for the older Dot 2 unless you add external speakers), or perhaps just to send the sound into another room without moving its source.

There can be setup issues—a mid-2011 Mac Mini paired but couldn’t keep a connection open reliably enough to play audio to an Echo Dot 3 but *did* play to an Echo Dot 2 (but it was not able to play to an “aggregate device” of two of them even though it could play to either one, and a little ‘choppiness’ was sometimes in the audio, and if it had been connected too long it might fail to play until rebooted).

Our Raspberry Pi devices could all pair once I figured out the exact commands that were necessary to “kludge” it, which are now in a utility called `player.py` distributed with my [Gradint](https://ssb22.user.srcf.net/gradint/) vocabulary-practice program.

A 2019 MacBook Pro was able to use two nearby Echo Dots as a stereo set—in Audio MIDI Setup create an “Aggregate device” with left assigned to channel 1 and right to channel 4, turn down the ‘wrong’ channel on each device and increase the overall volume. This did not work to another room though (range issues).

Pairing to a single Echo Dot worked from Amazon’s own Kindle Fire tablet and from a Samsung S21 phone, which can also pair to two devices at a time, but cannot turn down the ‘wrong’ channels on each device (and neither can the Dot itself—at least not unless you connect an external speaker and rig it to get only one of the two channels), and pairing *mostly* worked from a Samsung S9 phone.

If you do make Bluetooth work, you can still ask the Echo to change the volume or to answer simple questions (like “what is the time”) while Bluetooth is connected, but if you ask it to play other audio then it will disconnect from Bluetooth first and you must reconnect if you want it back later (it seems there are some exceptions to this depending on which “skill” is playing the audio).

You will *not* be able to combine Bluetooth input with the Echo Dot 3’s “stereo pairing” function instead of driving each device separately: the “stereo pairing” is reserved for the Dot 3’s own audio.

You can temporarily suppress the Bluetooth “now connected to” messages by turning off “Announcements” in the compulsory Alexa ‘app’ under the device’s Settings / Communication, and rebooting the Dot. But this does also have the effect of exempting it from manually-initiated site-wide announcements, and the “connected” messages can reappear after a few hours, plus the beeps are still present.

The above is based on my experience and is not legal advice.

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Amazon Echo Dot is a trademark of Amazon Technologies, Inc.
Android is a trademark of Google LLC.
AWS is a trademark of Amazon Web Services, Inc.
Bluetooth is a registered trademark held by the Bluetooth Special Interest Group.
Git is a trademark of the Software Freedom Conservancy.
Mac is a trademark of Apple Inc.
Python is a trademark of the Python Software Foundation.
Raspberry Pi is a trademark of the Raspberry Pi Foundation.
Samsung is a registered trademark of Samsung.
Sonos is a trademark of Sonos, Inc.
Spotify is a trademark of Spotify Ltd.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
