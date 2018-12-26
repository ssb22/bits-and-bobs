# Simple XML to files in "band"-like notation
# e.g. for https://ghr.nlm.nih.gov/download/ghr-summaries.xml
# Silas S. Brown 2018, public domain

import sys, pprint, os, unicodedata
if sys.stdin.isatty(): sys.stderr.write("Waiting for input on stdin...\n")
from xml.parsers import expat

os.system('rm -rf /tmp/txtout')
os.mkdir('/tmp/txtout')
os.chdir('/tmp/txtout')

def ignore(name):
    if name.startswith("html:") and not name=="html:p":
        return name[5:]

writingTo = [] ; writingStack = [] ; countsStack = [{}]
def StartElementHandler(name,attrs):
    try: name = str(name)
    except UnicodeEncodeError: pass
    if ignore(name): return CharacterDataHandler("<"+ignore(name)+">")
    newL = []
    global writingTo
    writingTo.append(("%s(%d)"%(name,countsStack[-1].get(name,1)),newL))
    writingStack.append(writingTo)
    writingTo = newL
    countsStack[-1][name]=countsStack[-1].get(name,1)+1
    countsStack.append({})
def EndElementHandler(name):
    if ignore(name): return CharacterDataHandler("</"+ignore(name)+">")
    global writingTo
    writtenTo,writingTo = writingTo,writingStack.pop()
    for k,v in countsStack.pop().items():
        if v==2: # only one: can strip out number
            for i in xrange(len(writtenTo)):
                if writtenTo[i][0].startswith(k+"(1)"):
                    writtenTo[i]=(k+writtenTo[i][0][writtenTo[i][0].index(')')+1:],writtenTo[i][1])
    if all(type(i)==tuple for i in writtenTo):
        # (name1,[(name2,..),(name3,..)] -> (name1/name2,..),(name1/name3,..)
        writingTo = writingTo[:-1] + [(writingTo[-1][0]+"/"+i[0],i[1]) for i in writtenTo]
    if not writingStack: # top-level close: final output
        lastFname = None
        for k,v in writingTo:
            k = k[k.find('/')+1:] # ignore top-level tag name (this is a no-op in trivial case where no slash)
            if type(v)==list and len(v)==1: v = v[0]
            if type(v)==unicode: v=v.encode('utf-8')
            if type(k)==unicode: k=k.encode('utf-8')
            if '/' in k:
                fname,band = k.split('/',1)
                if not fname == lastFname:
                    v2 = v.replace(' ','-').replace('/','-')
                    def zapAccents(f): return u''.join((c for c in unicodedata.normalize('NFD',f.decode('utf-8')) if not unicodedata.category(c).startswith('M'))).encode('utf-8') # accents in filenames confuse some emacs grep setups
                    fn = zapAccents(fname.split('(')[0]+'/'+v2)
                    if os.path.exists(fn): fn=zapAccents(fname+'/'+v2)
                    try: os.mkdir(fn[:fn.index('/')])
                    except: pass # exists
                    sys.stdout = open(fn,'w')
                    lastFname = fname
                k = band
                if '/' in k:
                    k0,k1 = k.split('/',1)
                    if k0.startswith(k1[:min((k1+'/').index('/'),(k1+'(').index('('))]) or ('/' in k1 and k0.endswith("-list")): k = k1 # simplify band names x-list/x(1) etc
            print k+":",v
def CharacterDataHandler(data):
    try: data = str(data)
    except UnicodeEncodeError: pass
    if not writingTo: return writingTo.append(data)
    elif type(writingTo[-1]) in [str,unicode]:
        writingTo[-1] += data ; return
    elif not data.strip(): return
    assert 0,"Unexpected cdata between items: "+repr(data)

parser = expat.ParserCreate()
parser.StartElementHandler = StartElementHandler
parser.EndElementHandler = EndElementHandler
parser.CharacterDataHandler = CharacterDataHandler
parser.Parse(sys.stdin.read(),1)
