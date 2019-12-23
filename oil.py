#!/usr/bin/env python2

# Python script to run the simulations for
# http://ssb22.user.srcf.net/elec/oil.html

# radiant heat due to lack of loft insulation ?
# (+ not rm'ing so much moisture & therefore bettr ??)

# http://web.archive.org/web/20140702232424/http://www.paulanthonywilson.com/blog/dyson-hot-review-a-scientific-approach/
# didn't wait long enough for cool-down ?  (only 1 reading)
# NB it's "race to 22deg in 20mins then off", not continuous?
# (AM09 review, most expensive whole-room one)

# h = q / deltaT, h: heat transfer coefficient, W/(m2 K)
# q = W/m2
# Air: h = 10 to 100 W/(m2K)

# If want to heat whole room (not just a spot) :
# total thermal conductance (watts per kelvin)
# try 15 for the oil rad (as heats up quite a lot while delivering 400W), 200 for the room

def simulate_heating_element(watts,onTemp,offTemp,medium,seconds=3600):
    # (NB onTemp,offTemp specified as deltas above 0=start)
    on = False ; totalOut = 0
    for second in xrange(seconds):
        if not on and medium.temp() <= onTemp: on = True
        elif on and medium.temp() >= offTemp: on = False
        if on:
            joules = watts # * 1 second
            medium.add(joules)
            totalOut += joules
        print second,
        medium.simulate_losses()
    for second in xrange(seconds,5400): # extra 30min cooldown
        print second, ; medium.simulate_losses()
    print "#",totalOut/3600000.0,"kWh consumed"
class Medium:
    def __init__(self, J_per_K, W_per_K, nextMedium):
        self.heatCap = J_per_K # likely to change with temperature but this should do for now
        self.conductance = W_per_K # of wall to next medium
        self.nextMedium = nextMedium
        self.joulesAdded = 0
    def add(self,J): self.joulesAdded += J
    def temp(self): return self.joulesAdded * 1.0 / self.heatCap
    def simulate_losses(self):
        deltaT = self.temp() - self.nextMedium.temp()
        joules_out = self.conductance * deltaT # * 1 sec
        self.joulesAdded -= joules_out
        self.nextMedium.add(joules_out)
        print ("%.2f" % (self.temp(),)),
        self.nextMedium.simulate_losses()
class Outside:
    def add(self,J): pass
    def temp(self): return 0
    def simulate_losses(self): print
# going to need heat capacity in J/K also
# .temp() .add(J) .simulate_losses()

# try simulating 'unheated room before the outside' also ?
# (or would that just factor into the insulation calcs)

# 1000J/Kg/K
# 1.225 kg/m3, 30 m3

#simulate_heating_element(2000,49,50,Medium(20000,15,Medium(40000,200,Outside()))) # settles on 3.4 degrees ?? need more than 50?  runs <50% of time (or is the 15 too small)
#simulate_heating_element(2000,19,20,Medium(40000,200,Outside())) # stuck on 9.9

# try better insulation to outside (for comparing heaters) :
#simulate_heating_element(2000,49,50,Medium(20000,30,Medium(40000,100,Outside()))) # reaches 11.4, 1.34kWh
#simulate_heating_element(2000,11,12,Medium(40000,100,Outside())) # same average for comparison, 1.24kWh
#simulate_heating_element(2000,11.4,12.4,Medium(40000,100,Outside())) # same minimum, 1.27kWh, both better than oil ??

# should assume 4deg hysteresis for simple thermostat? (needed for life expectancy of the heater)
# (room thermostat's switching differential/hysteresis is typically 1C)
#simulate_heating_element(2000,48,52,Medium(20000,30,Medium(40000,100,Outside()))) # 11.5/11.6, 1.34kWh
#simulate_heating_element(2000,11.5,15.5,Medium(40000,100,Outside())) # same minimum = 1.47kWh (10% higher)
#simulate_heating_element(2000,9.5,13.5,Medium(40000,100,Outside())) # same average = 1.22kWh (lower), but drops temp

#simulate_heating_element(2500,48,52,Medium(20000,30,Medium(40000,200,Outside()))) # 1.5kWh consumed
#simulate_heating_element(2000,6.5,10.5,Medium(40000,200,Outside())) # stuck on 9.9 anyway, 2kWh consumed (1500W=1.5kWh)
#simulate_heating_element(2500,6.5,10.5,Medium(40000,200,Outside())) # 1.8kWh consumed (20% extra)
#raise SystemExit

import sys,os
#sys.stdout = open("sim1.txt","w");simulate_heating_element(2000,48,52,Medium(20000,30,Medium(40000,100,Outside()))) # 11.5/11.6, 1.34kWh
#sys.stdout = open("sim2.txt","w");simulate_heating_element(2000,11.5,15.5,Medium(40000,100,Outside())) # same minimum = 1.47kWh (10% higher)
# try with worse insulation:
# U-value = W/m2/K; if all brick, 2*2*(5*3+3*2+5*2)=124, divide by 10 if gd insulation (but NB effect of windows etc)
sys.stdout = open("sim1.txt","w");simulate_heating_element(2500,48,52,Medium(20000,30,Medium(40000,200,Outside()))) # 1.51kWh
sys.stdout = open("sim2.txt","w");simulate_heating_element(2500,6.5,10.5,Medium(40000,200,Outside())) # 1.81kWh (20% extra)
sys.stdout = open("sim3.txt","w");simulate_heating_element(2500,26,31,Medium(20000,30,Medium(40000,100,Outside()))) # 0.82kWh (better insulation requires lower setting to get the 6.5C)
sys.stdout = open("sim4.txt","w");simulate_heating_element(2500,6.5,10.5,Medium(40000,100,Outside())) # 0.9kWh (10% extra)
sys.stdout = open("sim5.txt","w");simulate_heating_element(1250,26,31,Medium(20000,30,Medium(40000,100,Outside()))) # 0.77kWh (0.9kWh is now 17% extra with reduced element wattage)
sys.stdout = open("sim6.txt","w");simulate_heating_element(2500,42,46,Medium(20000,30,Medium(10000,1000,Medium(30000,200,Outside())))) # back to bad insulation and only care about the air near the radiator (very rough simulation), slightly lower setting to get the 6.5C, 1.3kWh
sys.stdout = open("sim7.txt","w");simulate_heating_element(2500,6.5,10.5,Medium(10000,1000,Medium(30000,200,Outside()))) # 1.52kWh = 17% extra
# non-thermostat try (against sim6) :
sys.stdout = open("sim8.txt","w");simulate_heating_element(400,65,105,Medium(10000,1000,Medium(30000,200,Outside())))
sys.stdout = open("sim9.txt","w");simulate_heating_element(800,65,105,Medium(10000,1000,Medium(30000,200,Outside())))
sys.stdout = open("sim10.txt","w");simulate_heating_element(1200,65,105,Medium(10000,1000,Medium(30000,200,Outside())))
sys.stdout = open("sim11.txt","w");simulate_heating_element(2500,58,62,Medium(20000,30,Medium(10000,1000,Medium(30000,200,Outside()))),1240) # heat up to 9C near heater, 0.74kWh, >=6.5C between t=636 and t=1672
sys.stdout = open("sim12.txt","w");simulate_heating_element(2500,42,46,Medium(20000,30,Medium(10000,1000,Medium(30000,200,Outside()))),1672) # for comparison (same heater at lower setting for longer, >=6.5 from 899 to 1752, 0.71kWh)
sys.stdout = open("sim13.txt","w");simulate_heating_element(1200,65,105,Medium(10000,1000,Medium(30000,200,Outside())),2200) # 0.73kWh
os.system("(echo 'set terminal png medium x000000 xffffff size 320,240 enhanced';echo \"set output 'oil1.png'\";echo 'set lmargin 0';echo 'set rmargin 0';echo 'set tmargin 0';echo 'set bmargin 0';echo 'set format x \"\"';echo 'set format y \"\"';echo 'set xrange [0:5400]';echo 'set yrange [0:55]';echo \"plot 'sim1.txt' using 1:2 title '' with lines,'sim1.txt' using 1:3 title '' with lines,'sim2.txt' using 1:2 title '' with lines\")|gnuplot")
os.system("(echo 'set terminal png medium x000000 xffffff  size 320,240 enhanced';echo \"set output 'oil2.png'\";echo 'set lmargin 0';echo 'set rmargin 0';echo 'set tmargin 0';echo 'set bmargin 0';echo 'set format x \"\"';echo 'set format y \"\"';echo 'set xrange [0:5400]';echo 'set yrange [0:55]';echo \"plot 'sim3.txt' using 1:2 title '' with lines,'sim3.txt' using 1:3 title '' with lines,'sim4.txt' using 1:2 title '' with lines\")|gnuplot")
os.system("(echo 'set terminal png medium x000000 xffffff  size 320,240 enhanced';echo \"set output 'oil3.png'\";echo 'set lmargin 0';echo 'set rmargin 0';echo 'set tmargin 0';echo 'set bmargin 0';echo 'set format x \"\"';echo 'set format y \"\"';echo 'set xrange [0:5400]';echo 'set yrange [0:20]';echo \"plot 'sim6.txt' using 1:3 title '' with lines,'sim6.txt' using 1:4 title '' with lines,'sim7.txt' using 1:2 title '' with lines,'sim7.txt' using 1:3 title '' with lines\")|gnuplot")
os.system("(echo 'set terminal png medium x000000 xffffff  size 320,240 enhanced';echo \"set output 'oil4.png'\";echo 'set lmargin 0';echo 'set rmargin 0';echo 'set tmargin 0';echo 'set bmargin 0';echo 'set format x \"\"';echo 'set format y \"\"';echo 'set xrange [0:5400]';echo 'set yrange [0:20]';echo \"plot 'sim6.txt' using 1:3 title '' with lines,'sim8.txt' using 1:2 title '' with lines,'sim9.txt' using 1:2 title '' with lines,'sim10.txt' using 1:2 title '' with lines\")|gnuplot")
os.system("(echo 'set terminal png medium x000000 xffffff  size 320,240 enhanced';echo \"set output 'oil5.png'\";echo 'set lmargin 0';echo 'set rmargin 0';echo 'set tmargin 0';echo 'set bmargin 0';echo 'set format x \"\"';echo 'set format y \"\"';echo 'set xrange [0:3000]';echo 'set yrange [0:10]';echo \"plot 'sim11.txt' using 1:3 title '' with lines,'sim12.txt' using 1:3 title '' with lines,'sim13.txt' using 1:3 title '' with lines\")|gnuplot")
