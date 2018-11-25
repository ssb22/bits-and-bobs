#!/usr/bin/env python2

# Simple script that takes XML (or non-XML) files,
# one record per line, and generates candidate entries
# for a word index into that data.  Some of the entries
# will be of low quality and should be deleted.

# Silas S. Brown 2018 - public domain

mark_down_xml = True
wordContext = 3 # num words on each side
max_phraseLen = 3
min_records_multiPhrase = 2 # multi-word phrase must match at least this number of different records to be indexed
stop_words = set(["a","all","are","an","and","at","be","but","by","for","if","in","the","this","to","too","some"]) # etc
assert all(x==x.lower() for x in stop_words)

import sys, re

def candidate_phrases(words):
    for phraseLen in xrange(1,max_phraseLen+1):
        for start in xrange(0,len(words)-phraseLen):
            w = words[start:start+phraseLen]
            if phraseLen>1 and not(all(x[0].isalpha() and x[-1].isalpha() for x in w)): continue # don't cut across starting quotes, commas, etc (but hyphens in middle OK)
            if not all(any(x.isalpha() for x in ww) for ww in w): continue # every word must have at least one alphabetical char for the phrase to make sense
            if all(keywordify(ww) in stop_words for ww in w): continue
            yield (start,phraseLen)

def capsInitial(w):
    # ignore open-quote etc before 1st letter
    for i in xrange(len(w)):
        if w[i].isalpha():
            return w[:i]+w[i].upper()+w[i+1:]
    return w

def keywordify(w):
    start,end = 0,len(w)
    for i in xrange(len(w)):
        if w[i].isalpha():
            start = i ; break
    for i in xrange(len(w)-1,start-1,-1):
        if w[i].isalpha():
            end = i+1 ; break
    return w[start:end].lower()

def context(words,wordNo,phraseLen=1):
    a,b = max(0,wordNo-wordContext),min(len(words),wordNo+phraseLen+wordContext)
    r = []
    if a: r.append("...")
    r += [w.lower() for w in words[a:wordNo]]
    r += [capsInitial(w) for w in words[wordNo:wordNo+phraseLen]] # TODO: syntax-highlight in some way? (if suitable output format)
    r += [w.lower() for w in words[wordNo+phraseLen:b]]
    if b < len(words): r.append("...")
    return " ".join(r)

mDict = {}    
lines = sys.stdin.read().decode('utf-8').split('\n')
if mark_down_xml: lines2 = [re.sub("<[A-Za-z/][^>]*>","",l) for l in lines]
else: lines2 = lines
for kwds,orig in zip(lines2,lines):
    kwds = kwds.split()
    for start,phraseLen in candidate_phrases(kwds):
        c1 = " ".join(keywordify(k) for k in kwds[start:start+phraseLen])
        c2 = context(kwds,start,phraseLen)
        key = (phraseLen,c1)
        if not key in mDict: mDict[key] = set()
        mDict[key].add((c2,orig))
for (phraseLen,c1),cList in mDict.items():
    if phraseLen==1: continue
    if not (phraseLen,c1) in mDict: continue # already deleted on a previous iteration of this loop
    origLineSet = set(y for x,y in cList)
    if len(origLineSet) < min_records_multiPhrase:
        del mDict[(phraseLen,c1)] ; continue
    for s in xrange(phraseLen):
        for e in xrange(s+1,phraseLen+1):
            if (s,e) == (0,phraseLen): continue
            k = (e-s," ".join(c1.split()[s:e]))
            if k in mDict and set(y for x,y in mDict[k])==origLineSet: del mDict[k] # no point listing the shorter phrase if all its entries are duplicated by the longer one, and we can have 'B: see A B' entries in the final UI (TODO: do this even if MOST of its entries are duplicated? but we may or may not have chosen sensible continuation words etc)
out = []
for (phraseLen,c1),cList in mDict.items():
    for c2,c3 in cList:
        out.append((c1,c2,c3))
for c1,c2,c3 in sorted(out):
        print (c1+"\t"+c2+"\t"+c3).encode('utf-8')
