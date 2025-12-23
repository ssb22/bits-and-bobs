
from https://ssb22.user.srcf.net/elec/ct.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/elec/ct.html) just in case)

# Current-transformer “energy monitors”

From around 2007 to 2010 several UK electricity boards and other organisations provided CT-based “energy monitors” with various names that all ran essentially the same program from Current Cost (HK) Ltd on a PIC18F85J90 microcontroller.

## Overestimating non-resistive loads

A limitation that must be understood if you’re trying to measure small loads is this: any monitor that relies only on putting a “clamp” around a mains wire to measure its current, must *assume* that the alternating voltage is in-phase with the alternating current (i.e. power factor 1). This is correct for high-power resistive loads like heaters, but loads that are more “reactive” (inductive or capacitive) will cause a phase-shift between the voltage and the current (so peak current is *not* at the time of peak voltage), and CT-based monitors (which assume this current peak *is* at the time of peak voltage) might calculate an apparent power consumption many times higher than the real one.

For example, some (but not all) types of mains-connected smoke alarm use a simple capacitive voltage divider (two capacitors connected in series) to get a low-voltage power supply. As capacitors charge fastest when they’re empty, the current could lead the voltage by almost a quarter-cycle, causing the CT monitor to get it wrong by a factor of 10 or so.

(A less-serious inaccuracy is, the monitor might be 10% wrong if it can’t account for normal voltage fluctuations on the line. In theory a more advanced monitor could measure voltage fluctuations through its own power supply, but there’d be no *point* if it’s using a battery-powered transmitter with only enough power to transmit an average current every so often—without precise high-resolution time-correlated values of both voltage and current, it can’t correct the larger error caused by the bad power factor of some small loads.)

The real power consumption is required to be reasonably-accurately measured by the billing meter, so you’ll have to read *that* to be sure (see [converting imp/kWh to watts](imp.md)).

Nevertheless a CT-based monitor (if you can find one that still works) could be used if the actual meter is not conveniently accessible (e.g. if it’s in an outside cabinet and the weather is bad), and should give a good reading for high-load items like cooking and heating.

## Usage

The “Current Cost” monitors were often supplied without instructions or with only vague ones, so here are some notes:
* Pairing the 433MHz ISM/SRD signal: long-press button on transmitter (requires pen or similar) and long-hold the Down key. Once paired, the transmitter’s clamp *normally* goes around meter cable 4. If that’s too cramped, you could try cable 1 but you’ll then be measuring the consumption of the meter itself as well.
  * **If your meter has a cable 5** then it probably means the storage-heater circuit is switched within the meter itself, rather than by a separate relay, and you’ll need *two* sensors to measure both—cable 4 for non-storage heater use and cable 5 for storage-heater use (although sometimes the cable 4 sensor will pick up 5–10% of the cable 5 current as well, suggesting [seriously under-performing storage heaters](e7.md) if that’s all you’re measuring)—but you *could* just put it around cable 1 and put up with having to deduct the meter’s own consumption (you’ll have to deduct things anyway if you have a capacitive smoke-alarm load as mentioned above), or, if cable 1 is too close to the board for the clamp to fit around it, you *might* have some success if you can put the clamp around cables 4 and 5 *together* (this is possible only if the clamp is large—some models of energy monitor have clamps that fit just one cable).
* Long-hold: Up to set currency and normal rate, Up+Down to set low rate and times (to 15mins), Square (marked “OK” on some models) to set clock
* The “cost per month” etc assumes consumption stays at the *current* rate, which is *not* meaningful for short-use appliances like kettles
* Less than 10W is displayed as 0 (you can measure small devices by first creating a higher base load; monitor itself takes about 1W)
* Transmitter batteries need replacing after a few years (size D)
* Clock can lose accuracy (and won’t run during power loss); don’t know about thermometer accuracy
* Some have an undocumented Ethernet-like RJ45 port on the bottom which is actually a serial XML-like output running at 57600-baud 8N1 (the non-rebranded product comes with an appropriately-wired USB-serial converter)
* A common reason for eventual hardware failure (apart from bad transmitter batteries) is worn-out connections within the receiver, which can affect button sensitivity, signal reception, and/or LCD segment fading (the latter can sometimes be temporarily revived by applying strong pressure around its inner border, especially at the bottom). It seems few units still work after 10 years, even if unused.

(See also [How to use Economy 7 effectively](e7.md) and my [energy deals coherence checker](https://ssb22.user.srcf.net/elec/))

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Ethernet was a trademark of Xerox Corporation but it was relinquished in 1982.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
