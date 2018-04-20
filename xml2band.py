# e.g. for https://ghr.nlm.nih.gov/download/ghr-summaries.xml
# public domain

import sys, pprint
from xml.parsers import expat

writingTo = [] ; writingStack = []
def StartElementHandler(name,attrs):
    try: name = str(name)
    except UnicodeEncodeError: pass
    if name.startswith("html:"): # just treat as data
        return CharacterDataHandler("<"+name[5:]+">")
    newL = []
    global writingTo
    writingTo.append((name,newL))
    writingStack.append(writingTo)
    writingTo = newL
def EndElementHandler(name):
    try: name = str(name)
    except UnicodeEncodeError: pass
    if name.startswith("html:"): # just treat as data
        return CharacterDataHandler("</"+name[5:]+">")
    global writingTo
    writtenTo,writingTo = writingTo,writingStack.pop()
    assert name==writingTo[-1][0], "tag mismatch"
    if all(type(x)==tuple for x in writtenTo) and len(set(n for n,_ in writtenTo))==1:
        # all sub-names are identical: probably redundant
        writingTo[-1]=(name,[x[1] for x in writtenTo])
        if all(type(x)==dict and len(x.keys())==2 and set(x.keys())==set(writingTo[-1][1][0].keys()) for x in writingTo[-1][1]):
            # e.g. {'db':X,'key':Y},{'db':X,'key':Y,...}
            # the 'db' and 'key' headings prob redundant
            writingTo[-1]=(name,[(sorted(i.items())[0][1],sorted(i.items())[1][1]) for i in writingTo[-1][1]])
    elif all(type(x)==tuple for x in writtenTo) and len(set(n for n,_ in writtenTo))==len(writtenTo):
        # all sub-names are unique: can be a dict
        writingTo[-1]=(name,dict(writtenTo))
        for k,v in writingTo[-1][1].items()[:]:
            if type(v)==list and all(type(i)==tuple and len(i)==2 and not i[0] in writingTo[-1][1] and len(i[0])<20 for i in v):
                # list of (k,v) could just go in the dict
                del writingTo[-1][1][k]
                for i0,i1 in v:
                    writingTo[-1][1][i0] = i1
            elif type(v)==list and len(v)==1:
                # list of 1 item: don't need wrap in list
                writingTo[-1][1][k] = v[0]
    elif len(writtenTo)==1 and type(writtenTo[0]) in [str,unicode]:
        # (name, ["string"]) -> (name, "string")
        writingTo[-1] = (name,writtenTo[0])
    if not writingStack:
        pprint.PrettyPrinter(indent=2).pprint(writingTo)
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
