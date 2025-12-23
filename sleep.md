
from https://ssb22.user.srcf.net/elec/sleep.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/elec/sleep.html) just in case)

# Magnetic field physics: is your phone charger really killing you?

Some people are concerned that charging a mobile device in a bedroom while sleeping is a health risk due to excessive AC magnetic fields. Should we be worried? Let’s do the maths.

For a pair of long, straight wires carrying current in opposite directions, if the distance between you and the wires is significantly greater than the distance between the pair of wires themselves (which is almost certainly the case if the wires are barely a millimetre apart and you’re not touching them), then the magnetic field strength in *amperes per metre* (the H-field in Maxwell’s equations) is given by:

> Twice the current flowing in the wires (in amps), multiplied by the wires’ separation distance (in metres, probably about 0.001), divided by the square of the distance between you and the wires (in metres).

You can get this from a paper in the IEEE Transactions on Space Electronics and Telemetry, Volume 10 number 4 (December 1964), pages 154-158, where we read how NASA’s Alberta Alksne worked out how much magnetic field would be coming from the wires in a spacecraft. Looking at his Equation 7, the two components of the field are calculated by:
* the current flowing in the wires
* multiplied by the wires’ separation distance
* divided by the square of the distance between you and the wires
* multiplied by:
  * for the X direction, -4 * *cos t* * *sin t* (because, for some angle *t*, *x=r cos t* and *y=r sin t*, so *xy/r^2* is just *cos t* * *sin t*, and Alksne’s wire-separation distance is *twice* the value of *a*, see his Fig. 1, so we halve the -8 to compensate),
  * and, for the Y direction, +2 - 4*(*sin t*)^2 (because r^2=x^2+y^2 by Pythagoras, so x^2-y^2 = r^2 - 2y^2, so we have +2 * (*r* ^2-2*(*r sin t*)^2)/ *r* ^2 and the *r* cancels out upon simplification),
  * so the multiplier for the overall magnitude is sqrt((4 * *cos t* * *sin t*)^2 + (2 - 4*(*sin t*)^2)^2)
  * and it can be shown (numerically if you like) that this is always equal to 2 no matter what the value of *t*.

## Twisted wires

Alksne found the field can be increased if the wires are twisted. House wiring is not usually twisted, but as charging cables can *become* slightly twisted, let’s look at twisted wires as a worst case.

Alksne’s Fig.2 shows that the worst possible case is when the length of the twist is about 10 times the distance between you and the wire. In this case you might need to add nearly 10% extra to the field strength on the X axis, although it drops in other directions and with other twist combinations. So twists *usually* work in your favour, but if we’re being really pessimistic, we’d better say you might be ‘unlucky’ enough for the wires to be twisted in such a way that 10% is added, so we have:

> 2.1 * amps * about 0.001 / distance^2

although that extra 10% is probably within the error bars of the “about 0.001 separation” anyway, unless you pull apart your wiring to measure it exactly (please don’t!)

## Teslas, gauss and milligauss

To get from amps per metre to teslas, we need to multiply by our magnetic permeability. Since we’re not magnetic people, this is probably going to be similar to the magnetic permeability of free space, or 4*pi*10^-7. Putting that into our equation, we get, for a ~1mm-separated twisted pair:

> teslas = 2.64e-9 * amps / distance^2

and, since a tesla is about 10,000 gauss,

> gauss = 2.64e-5 * amps / distance^2

or, since discussions of EMF health risks usually refer to *milligauss*,

> milligauss = 0.0264 * amps / distance^2

As we seem to be just fine in the Earth’s “DC” magnetic field of 250 to 650 milligauss, which would take a massive 10,000-25,000 amps to match using DC current in a 1mm-separated pair of contraflow cables a metre away (don’t try that at home—it’ll burn the wires and possibly your house, which is *definitely* a bigger health risk than the magnetic field), I assume the only thing we *might* have to worry about (with pairs of cables in contraflow) is the “AC” part of the field.

Phone chargers typically take more current during the phone’s “fast charge” phase and less in its “trickle charge” phase. The new “Quick Charge” chargers are supposed to get the fast phase done in *minutes*, which makes them less likely to be relevant in “charging while you sleep” calculations, so let’s look at older chargers’ fast phases. If the charge is taking place over a USB cable then the output voltage will be 5V (USB standard), and the output current is typically a maximum of 1A (but iPad chargers can do 2A), which means 5 (or 10) watts; since the charger is inefficient, you probably have to double this to 10 (or 20) watts on the mains input side, which at 240V gives 0.04 (or 0.08) amps; it’ll be double that in America where the mains is only 120V (watts = volts x amps). Therefore, for the *input* to the phone charger, we’re looking at:
* 0.001 (or 0.002) milligauss for a 1mm-separated 240V wire at 1 metre (Americans have to double this for 120V)
* up to 0.008 milligauss if that wire is only 50cm away
* up to 0.2 milligauss if that wire is only 10cm away
* double again if it’s separated by 2mm instead of 1mm
* double again if it’s a big one separated by 4mm

and we’re *still* not up to the “1 milligauss” limit recommended by the Bioinitiative Report of 2012.

But what about the current coming *out* of the phone charger, which has a lower voltage but higher current? It’s *supposed* to be DC, but it *can* also have ripples or (if the charger is a cheap half-wave rectifier) pulses. I don’t know if a *pulsed* DC field will be as bad as an AC field, but let’s assume it is and check:
* for a 1-amp charger, 0.026 milligauss at 1m (double for 2-amp, but hopefully a 2-amp charger won’t be so pulsed)
* increasing to 0.1 milligauss at 50cm, and 2.6 milligauss at 10cm

so if you’re worried about exceeding 1 milligauss while sleeping, then you won’t want to sleep within *10 centimetres* of an operating phone-charge cable, but you should be fine at 50cm, and shouldn’t have to worry about its mains input cable even if that one passes as near as 10cm (*unless* your house is wired in a ring main and the cable near you is part of the ring instead of a spur coming off it, in which case a wiring fault could cause current to flow around the ring instead of back where it came from, which means a different set of equations apply and the fields could be much higher, but thankfully that kind of setup is now quite rare; I think they stopped doing it that way when it caused too much interference with radios etc).

I’m not absolutely sure how that conference arrived at their “1 milligauss” figure, but I think it’s related to a 2008 study of Chinese children (Yang et al, Leukemia & Lymphoma 49(12):2344-2350) which looked at 123 patients and 135 healthy children and said the patients tended to be getting 1.4 milligauss from power lines near their houses, although nobody seemed to be made worse by communications transmitters (which run on a different frequency) or indoor appliances. (A previous study they cited by Maslanyj et al put the threshold at 4 milligauss and said indoor appliances account for *most* of it, so we can see where the “it matters more when you’re asleep” idea might have come from. Tissue repair happens more during sleep, and the bedroom appliances mentioned in the Chinese study—microwave ovens etc—are not typically in use during sleep.) Unfortunately Yang et al didn’t have the resources to quantify what percentage of *everyone living near power lines* got cancer, as opposed to what percentage of everyone *not* living near power lines did so, so the study still doesn’t tell us *how big* a risk factor the power lines are, but it does seem to show *some* risk (although the original data doesn’t seem to be available so we can’t check the exact details of their statistical tests).

I’ve separately seen the figure “0.2 milligauss” mentioned as a slight concern, but I haven’t seen anything concrete as to how this was arrived at. (The human brain itself produces a changing magnetic field, but only in the nanogauss range; that doesn’t mean we can cope *only* with nanogauss though.) If 0.2 milligauss is correct, then you can be concerned about sleeping 10cm away from a mains cable feeding a phone charger, but greater distances should still be OK.

So generally, a cable (whether mains or low-voltage) that’s involved only in charging a phone should be fine to sleep near to if it’s more than 10cm away.

## Night storage heaters

A gentle night-storage heater might charge itself using as little as 1 or 2 amps, but some use 10 amps or more. If you have one of the latter, you’d better make sure its cable is more than a metre away if the extra-cautious 0.2 milligauss figure is correct.

## A timer for phone charging?

I’ve seen published suggestions that plug-in timers be used to switch off phone chargers automatically after a few hours, to “save energy” once the charge is complete. That won’t work, because the power consumption *of the timer itself* will be similar to that of a charger supplying trickle charge (e.g. USB 100mA at 5V & 50% efficiency = 1W input)—so the small amount of energy “saved” by cutting power to the charger once charged is then used up by the timer that does it, and all else being equal I’d rather spend it on keeping a phone battery topped up than a timer running. A slightly better use of a timer, if you have [Economy 7](e7.md), is to *start* the charge later so that the higher-power “fast charge” phase falls on the off-peak period, but even if you’re disciplined enough to power the timer only at night you still won’t save *much*—perhaps a penny a week at 2017 prices, which could take over 25 years to redeem the cost of the timer (not counting the value of *your* time spent acquiring and maintaining it), and I’m inclined to question the value of energy-saving equipment whose pay-off period exceeds its life expectancy. An offpeak-only 3-pin socket would similarly not be worth the setup costs unless used for something considerably more substantial. If someone could modify a phone’s *firmware* to schedule its fast charges to the cheaper period, and get a million Economy 7 users to switch to the modified firmware without hassle, *then* perhaps some more serious savings could be made (collectively), but still there are much bigger priorities in the energy-saving department (transport, heating etc) and I’d rather see our thoughts applied to how to save on *those* first.

## Using a phone while charging it

In 2021 and 2022 some people from the Asia-Pacific region became concerned due to a short video distributed on social media which appears to show a non-contact voltage tester reacting to a phone’s charge cable, and still reacting if held above the phone or above the other hand of the person using the phone. But pausing the video shows it’s a misinterpretation to say the charge cable was somehow “charging up” the user—when being held over the person’s hand, the original charge cable was running *behind* that arm, so EMF was likely being detected *through* the body, not *from* it. The amounts are not stated but are likely small as shown above. The video was labelled “deceptive” by AAP and ARPANSA in May 2021.

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Any [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
