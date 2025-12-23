
from https://ssb22.user.srcf.net/gradint/dvr.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/gradint/dvr.html) just in case)

# Pen-sized digital voice recorders

![dvr.jpg](https://ssb22.user.srcf.net/gradint/dvr.jpg) One piece of electronics that used to be popular with Chinese students is the pocket digital voice recorder, known informally as a 录音笔 lùyīnbǐ “recording pen”. These devices can take an audio recording of a meeting and transfer it to a computer later via USB. I haven’t seen so many students with these lately, presumably because their tablets and smartphones can run [recording software](https://ssb22.user.srcf.net/setup/asound.html). But if your phone is old and cannot manage longer sessions without a bulky battery extender or similar, or if it records unwanted finger noises when also in use to look up words in a dictionary or whatever, then a separate recording “pen” might still be useful.

The problem with recording pens is **choosing one can be difficult**. Often they have no branding (or they can be rebranded by any company), and often they have either no model number at all, or a number that has since been re-used by a completely different product with lower specifications, and this makes it very difficult to make recommendations (if I say “I had a good experience with the such-and-such” and you try to buy it, you might well end up with a poor imitation). Furthermore, they don’t last forever, so you’ll need a new one from time to time, and the chances are when you *do* need a new one the supplier you used last time will have closed down so you’ll have to do the research all over again. Here are my notes if it’s any help (usual disclaimers apply).

## Check the format and bitrate

Original recording pens used a very low bitrate in a proprietary format that was read out very slowly by a proprietary USB-1.0 driver which required root access to a proprietary operating system (usually a contemporary version of Microsoft Windows) and it was generally awkward. Thankfully, most recent devices can record in standard formats and present themselves as standard USB mass storage devices to any computer running any software, but it’s worth checking the specification sheets for which recording format is used. If the sheets say it works in Mac and Linux as well as Windows, that’s a good sign that it’ll be a generic mass USB storage device, but not all manufacturers bother to say this (some will even say “Windows only” when what they actually mean is they supply a disc of Windows “extras” but the hardware itself can be connected to anything—but there’s often no way to guess that from the spec sheets).
* If the device presents itself to a computer as standard USB mass storage, that *doesn’t* make it a good idea to use it as a general file store: some devices have been known to use low-quality memory that exhibits occasional “bit flips”, which might be relatively benign for audio but serious for data. Best use the device for audio only, and use a separate “memory stick” if you need to carry data also.
* Beware that many devices say “MP3” because they can *play* MP3 files, but that doesn’t automatically mean they can *record* in MP3 format unless it says so explicitly. However, if it mentions WAV format, it can usually record in that.
* Similarly, some devices can play FM radio, but that doesn’t mean it can *record* from the radio unless it explicitly says so.
* I had one device (which plugs into a USB port without a cable—looks like a fat memory stick) which says it can record “32K WAV”. This turned out to mean a 16 kHz sample rate, sampled at 13 bits and compressed to 4 bits via IMA ADPCM (which can be decoded by `sox`), thus taking 64 kbps. It sounds just about bearable for voice, *if* the background noise is low enough or you are close enough to the sound source. This recorder would lose all of the current recording if the battery voltage gets too low.
* Devices that can record MP3 will likely have higher quality, thus not requiring such close proximity to the sound source (which generally makes the logistics easier if you’re trying to record a meeting or conference). However, finding such devices is more difficult.

## A voice recorder that can record in MP3 format

I bought this online in 2009 and it broke down in 2014; replaced in 2015 with a very similar product. I believe it originally came from Shenzhen, but it’s unbranded (the first one I had ended up being marked “UltraDisk” but I believe this was added later), and there’s no model number, so the only way I can suggest finding an exact replacement is to search for the exact contents of its specification sheet (the dimensions, weight and formats make surprisingly effective initial search criteria). I’ve written out the manufacturer’s specifications below (including the errors, which I hope they now keep so we can search for them!) and added my notes in the right-hand column.

### Older version (bought 2009)

What the spec sheet says - What it really means

Dimension:103mm*32mm*16mm

Weight: 28g - Dimensions: 103mm x 32mm x 16mm

Weight without battery: 28g (although one AAA battery doesn’t weigh much more)

Power supply:

A piece of AAA alkaline battery - Powered by one AAA battery. In my experience an 800mAh Ni-MH rechargeable works just fine if changed every 3 hours or so; it doesn’t have to be alkaline. I expect “a piece of” was a mistaken translation of 一块. If you do use alkaline, beware of gradual voltage drop: once the voltage drops below the level required to record, the device simply stops recording (and, unlike some other products, leaves the partial recording intact) but **still plays**. If you were recording from FM then the radio will continue to play through the earphones even after the recording has been abandoned, so you can’t rely on the fact that the radio is still playing to indicate the recording is still going: you have to check the display. If you use rechargeables then the voltage drop will probably be sudden enough for you to notice (and you should still get the abandoned recording), but it’s better to proactively change batteries during breaks etc before they get that low. (If you only have NiCd not NiMH and want to give your batteries a full discharge cycle, you can always complete that later.)

Flash memory:

FLASH 128MB ~ 2GB - Different capacities are available. The memory is formatted as a flash disk and can be read by a computer plugged in via a USB cable: it presents itself to the computer as a standard mass storage device.

The socket for the USB cable was the first thing to break on my recorder after 5 years of occasional use (perhaps 50 to 70 plug/unplug cycles). After that socket was broken, the only way to get sound out of the DVR was to have it play the audio in real-time with the computer recording. (The headphone socket was the next thing to break, followed by the controls.)

Record bit ratio:

LP 8 Kbps / SP 32 Kbps / HP 128 Kbps - These are the bitrates used by the 3 formats that the recorder supports. The “LP” mode records files in ACT format at 8 kilobits per second; “SP” records 32-kilobit (compressed) WAV files and “HP” records 128-kilobit MP3 files. If recording in an environment with background noise, it’s really best to use HP (MP3), otherwise you have to be quite close to the sound source (loudspeaker or whatever) to get a clear enough recording. Recording from FM radio is done in SP mode (it cannot be done in HP mode, presumably because the processor wouldn’t be able to decode FM and encode MP3 at the same time), but if the FM signal is clear then the reduced bitrate doesn’t usually matter for voice: when a conference venue transmitted its programme on low-power FM, I found an SP recording of the FM signal had comparable clarity to an HP recording from the microphone.

Recording time:

128MB:LP 35 hours/SP 8 hours/HP 2 hours

256MB:LP 70 hours/SP 17 hours/HP 4 hours

512MB:LP 140 hours/SP 35 hours/HP 9 hours

1GB: LP 280 hours/SP 70 hours/HP 17 hours

2GB: LP 560 hours/SP 140 hours/HP 34 hours - This is the theoretical total time that can be stored in the specified capacity if all your recordings are in the specified format (LP, SP or HP). It seems the figures have been rounded down (which is just as well because we need to remember filesystem overheads). They forgot to say that **there is also a maximum length of any one recording** which I believe is either 2.5 or 3 hours (the recorder stops after that), so you can’t just leave it somewhere to record a whole day without further operation.

FM Radio (selectable):

87.0MHz~108MHz - Some, but not all, of the units sold have FM capability (so if you want FM then be sure you’re getting one *with* FM: most English spec sheets would say “optional” instead of “selectable”). If your unit does has FM, this is the available frequency range. Recording from FM is possible (at 32kbps, see above); the headphone wire acts as the antenna (so you’ll need to plug in headphones).

Frequency response:

20Hz~20KHz - I’m not sure if this is for recording or for playing. If for recording, it must apply only to HP mode because it goes above the Nyquist limit of the other two formats. I haven’t tested the exact frequency response, but it seems fine for voice. For music, it depends on the quality of the microphone (if using an external one) and whether the recorder is too close to the source.

Signal noise ratio: 80db - This is their rating of the noise introduced by the device itself; in practice it is less relevant than the amount of background noise coming into the mic

Maximum output:

10mw(L) + 10mw( R ) - The power available to drive headphones at maximum volume. This isn’t much of a concern if the device is primarily being used to record rather than to play.

Supportsystem:Windows98/Me/2K/XP/Vista

(this is all printed without spaces) - In my experience the recorder connected via USB to *any* computer, including Mac and GNU/Linux. The supplied software to convert the “ACT” format (used by the lowest-quality recording mode) is Windows only, but that doesn’t matter if you avoid using the lowest-quality recording mode (and I can’t imagine why anybody would *want* to use that mode unless they’ll be away from a computer for a very long time).

Recording audio format: MP3 WAV ACT - See above. “ACT” seems to be a proprietary format: I suggest avoiding that mode and recording in either MP3 or WAV.

Music audio format: MP3 WMA - This is for playback. The device can also play back its WAV and ACT files.

There were two minor annoyances I haven’t mentioned above:
1. Use of the supplied external microphone usually resulted in occasional 217Hz “burst” noise from nearby GSM mobile phones; this was not the case with the internal mic, but then the recorder had to be positioned more carefully (most conference venues are not designed for good sound at floor level for example; seat level or armrest level might just about work, but I usually found myself putting my ear down to it to check what kind of sound it was getting)
2. When using the menu system (which by the way you have to read the instruction book to understand), the recorder will automatically switch off if you don’t press a key for a minute or so. This was most annoying if you were waiting to *start* a recording at the right moment and in highest quality, because, after switching back on, you either have to accept its default SP mode (lower quality) or else fumble around the menus to repeat your earlier selection (not so good if what you want to record is literally just about to start). Therefore I’d either keep the recorder “alive” by periodically pressing keys while waiting for the start, or else start it early and edit the file afterwards.

The internal microphone theoretically records in stereo (which I have not found to be very effective, but I’m not worried: I simply convert it to mono later to save space) and the recorder also came with a connector to intercept a landline telephone’s wire (I didn’t test this).

### Newer version (bought 2015)

Much the same as above, but with updated specifications:

What the spec sheet says - What it really means

Dimension: 102mm*28mm*14mm

Weight: 28g - As above (notice this one is *slightly* narrower)

Power supply: One piece of AAA alkaline battery 1.5V - Once again an 800mAh Ni-MH rechargeable worked; it didn’t need the full 1.5V. This version is also able to operate on USB power, but typical portable “Power Bank” products are *not* likely to be suitable, because the recorder draws so little current that the powerbank treats it as a phone that has finished charging and shuts down. The instructions call USB power “USB recharging” but my voltmeter registered 0.7V across the empty holder so an AAA is unlikely to be charged. If battery is knocked out during recording then the current recording is lost.

Flash memory: 1GB-4GB - I used `dd` to test the 4GB (3.7GiB) model and yes it really did read back that much random binary data without differences

Record bit ratio: LP 32Kbps / SP 128 Kbps / HP 192 Kbps - In this version, *all* recordings are IMA ADPCM-encoded WAV files. HP is 48kHz mono; SP is 16kHz stereo (thus 64 kbps per channel) and LP is 8kHz mono. The high sampling rate of HP does seem to make up for the simple encoding scheme which probably reduced their license fees.

Support system: Windows2000/XP/Vista/7 - Once again it’s a standard USB mass storage device that **does** work on non-Windows systems (Mac, GNU/Linux, etc). Perhaps this line was added because very old Windows systems need extra drivers.

Recording format: WAV - See above

The FM frequency range was no longer listed on the sheet. On mine, it was 76MHz-90MHz, the broadcast band of Japan, which only partially overlaps UK/Europe’s 87-108, but more frequencies are available via a software bug: scan down to 76 and stop, then try to auto-scan *lower* and it’ll search down to about 12 then wrap around to 114 or 160. FM is recorded at “SP” quality.

**Switching off VOS:** Page 7 of the instructions says that VAR (called VOS on the LCD) defaults to level 0, but mine came set to level 1. It also came with 2 brief recordings of Mandarin-speaking girls in a QA department, so perhaps somebody forgot to reset the chip. Never mind: to set it back to 0, start a test recording, stop it, and press the volume away from you until the display shows 00. This setting appears to be preserved across battery changes as long as the recorder had a clean shut-down (off button) before the change. Non-0 means in a quiet environment the recorder will automatically pause, hence deleting the speaker’s pauses and sometimes clipping the start of consonants that break silences, so I suggest making sure it’s set at 0.

(And I deleted the girls’ test recordings straight away—I didn’t want to repeat the 2008 “iPhone girl” incident in which a worker’s test picture became widely circulated. In this case it seemed my recorder was being tested by an apprentice who was checking with her supervisor about what other functions to test, but I didn’t quite catch all of her Mandarin words. Anyway, I’ve not only deleted it but also overwritten it with random data in my `dd` test, so she’s safe.)

## Avoid the “Mini DV” voice recorder

![dvrbad.jpg](https://ssb22.user.srcf.net/gradint/dvrbad.jpg)I was sent one of these by mistake. The company confirmed they’d made a shipping mistake and sent me the correct item at a reduced cost (seeing as returning the incorrect one to China would have been awkward). Meanwhile in the interests of science I looked at this but it was useless. Instead of an easily-swappable AAA battery, it’s driven from a limited-capacity “PL602030” which requires soldering skills to replace, and the one in my unit was bad (confirmed with multimeter, 0V even after an all-night charge at 4.8V). The device won’t operate while charging, so it was effectively just an unreliable USB stick.

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
iPhone is a trademark of Apple in some countries.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Mac is a trademark of Apple Inc.
Microsoft is a registered trademark of Microsoft Corp.
MP3 is a trademark that was registered in Europe to Hypermedia GmbH Webcasting but I was unable to confirm its current holder.
Windows is a registered trademark of Microsoft Corp.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
