#!/usr/bin/env python3

# fit 3 points to A ln (x-B) + C
# Silas S. Brown 2024 - public domain - no warranty

import scipy.optimize, re
from math import log
from statistics import mean
def logfit(x1,y1,x2,y2,x3,y3):
    # y1 = a ln (x1-b) + c
    # y2 = a ln (x2-b) + c
    # y3 = a ln (x3-b) + c
    # --------------------
    # y1-y2 = a ln ((x1-b) / (x2-b))
    # y1-y3 = a ln ((x1-b) / (x3-b))
    # (y1-y2)/(y1-y3) = ln((x1-b)/(x2-b))/ln((x1-b)/(x3-b))
    # ((x1-b)/(x3-b))**((y1-y2)/(y1-y3)) = (x1-b)/(x2-b)
    b = scipy.optimize.newton(lambda b:((x1-b)/(x3-b))**((y1-y2)/(y1-y3)) - (x1-b)/(x2-b),0)
    # b may not be exact, so use mean() for these:
    a = mean([
        (y1-y2)/log((x1-b)/(x2-b)),
        (y1-y3)/log((x1-b)/(x3-b))])
    c = mean([
        y1 - a*log(x1-b),
        y2 - a*log(x2-b),
        y3 - a*log(x3-b)])
    a = makeRound(a,[
        (lambda a:a*log(x1-b)+c,y1),
        (lambda a:a*log(x2-b)+c,y2),
        (lambda a:a*log(x3-b)+c,y3)])
    b = makeRound(b,[
        (lambda b:a*log(x1-b)+c,y1),
        (lambda b:a*log(x2-b)+c,y2),
        (lambda b:a*log(x3-b)+c,y3)])
    c = makeRound(c,[
        (lambda c:a*log(x1-b)+c,y1),
        (lambda c:a*log(x2-b)+c,y2),
        (lambda c:a*log(x3-b)+c,y3)])
    return a,b,c

def makeRound(param,funcsAndResults):
    # remove misleading accuracy (in base 10)
    denom = denomOf(param)
    while True:
        denom *= 10
        param2 = roundTo(param,denom)
        if not all(str(roundTo(func(param2),denomOf(result)))==str(result) for func,result in funcsAndResults): return param
        param = param2
def denomOf(n): return float(re.sub(r'^\-?0*','',re.sub('[1-9](?=.*1)','0',re.sub('[2-9](?=[0.]*$)','1',str(n)))))
def roundTo(n,denom): return denom*round(n/denom) if denom>=1 else round(n,-round(log(denom,10)))

if __name__=="__main__":
    import sys
    a,b,c = logfit(*[float(i) for i in sys.argv[1:]])
    print (f"{a}*math.log(x{-b:+g}){c:+g}")
