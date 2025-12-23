
from https://ssb22.user.srcf.net/elec/imp.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/elec/imp.html) just in case)

# Converting “1000 imp/kWh” to watts

The UK has seen three general kinds of domestic electricity meter: very old mechanical meters (with dials or mechanical counters) that have no lights, moderately-old digital meters that still need to be read, and now “smart” meters that transmit their readings automatically. The more recent two of these three (the moderately-old digital meters and the “smart” meters) both tend to have flashing lights, but the meaning of the lights is different.

On a “smart” meter, the meaning of the lights may vary with manufacturer, and in some cases indicates signal transmission status rather than energy use. But on a moderately-old digital meter (typically installed for consumption or microgeneration before some time in the 2010s), the light usually flashes a set number of times per kWh, typically 1000 imp/kWh. You can multiply the time between two flashes by 1000 to find the time it will take to “clock up” 1 kWh at the current usage rate, but if you’d rather have everything in watts (and you do not possess a wireless energy monitor, or there is insufficient wiring-board room to install one), then you can use:

Average kW = 3.6 / seconds per flash

(or, if you have a metronome, kW = 0.06*BPM)

For example:

Period - Wattage

1s (60 BPM) - 3.6kW

1.5s (40 BPM) - 2.4kW

2s - 1.8kW

3s - 1.2kW

4s - 900W

5s - 720W

6s - 600W

8s - 450W

10s - 360W

15s - 240W

20s - 180W

30s - 120W

1min - 60W

2min - 30W

For the rarer 800 imp/kWh meters, use kW = 4.5 / seconds per flash (or 0.075*BPM). In case there are any meters out there with other imp/kWh values, the general formula is kW = 3600/(imp/kWh) / seconds per flash (or 60/(imp/kWh) * BPM), but it seems 1000 imp/kWh is most common (at least in 2014).

I put up this page because there seemed to be some misinformation going around, for example:
* the idea that “imp” somehow stands for impedance on these meters (or “impressions”, but that misunderstanding is not as bad as “impedance”; meter data sheets say “impulses”),
* or that one flash of a 1000 imp/kWh meter means you’ve “used up one watt” (please stop guessing)—a flash of a 1000 imp/kWh meter does correspond to a watt-*hour* (3600J), but as a unit that’s not generally as useful as the kWh (3.6MJ), and the watt itself is a measure of *rate* (it’s a joule *per second*)—you can’t “use up one watt” unless you’re a circuit designer worrying about a power budget—kWh is to kW as miles is to miles-per-hour (one is something you can “clock up”, the other is the speed at which you’re doing so; I suppose the placement of the word “hour” might look inconsistent to people unfamiliar with SI units, since on their cars the unit for speed is the one that includes “hour”, whereas when measuring energy flow the unit for rate is the one that does *not* include “hour”—sorry if this is confusing).

If an imp/kWh light is lit continuously then this indicates **no** current flow (but some meters show this as no light rather than a continuous light). In some cases an extremely small current (such as a Raspberry Pi B+ playing audio to non-amplified speakers) will count as “no current”, but the meters are usually quite sensitive.

Some two-rate meters used in Economy 7 (e.g. 5246C) also have a second light, confusingly placed near the maximum-current label (e.g. 100A), which is always lit continuously when the off-peak circuit is energised, regardless of whether or not it’s being used. The primary imp/kWh light is the only one whose flashing or continuity indicates use or no use.

(See also [current-transformer “energy monitors”](ct.md), [how to use Economy 7 effectively](e7.md) and my [energy deals coherence checker](https://ssb22.user.srcf.net/elec/))

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Raspberry Pi is a trademark of the Raspberry Pi Foundation.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
