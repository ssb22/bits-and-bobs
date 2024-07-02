#!/usr/bin/env python3

"""DAPXlate - Dictionary-Assisted Pretrained Translate
  v0.2 (c) Silas S. Brown 2024, License: Apache 2

  - Uses a pretrained translator model online
    but adds specialist name translation from
    CedPane.  Does this by having the model handle
    placeholders for words we're sure we know how
    to translate ourselves from the dictionary.

    (Models can't always cope with pre-translated
     fragments in the target language, so it's
     necessary to use the placeholders.)

  PROBLEMS:

    - Relies on 'service as a software substitute'
      - and deep_translator appears to be using an
        undocumented API endpoint that could stop
        working at any time

    - Resulting translation still needs editing
"""

from deep_translator import GoogleTranslator as T
# (you could use another if you have an API key)
import re, sys, os

def read_CedPane(cedpane_file):
    "Extract specialist translations and names from CedPane"
    # 'here' + 'in' were words, don't want those
    # 'notice' probably don't want
    dups = set() # avoid translating if we're not sure
    e2c = {}
    for en,zh in [l.split("\t")[:2] for l in open(cedpane_file).read().split("\n")[1:-1]]:
        if "translation" in en or "incorrect" in en or re.search(r"\btypo\b",en): continue # alternate translation, old translation, typo, etc
        if "(" in en: continue # we don't want entries like "notice (on paper)" where the parens indicate it's a specific meaning (but TODO some entries with parens may be ok)
        if re.search("; [^A-Z]",en): continue # "here; in this region" probably shouldn't pull out "here", but ";" + abbreviation is probably OK, as is "Name; Name"
        # TODO: didn't include <p> (prob {..}) at start of sentence, regex seems ok, did model drop it?
        for en in [een.strip() for een in re.sub("[(][^)]*[)]","",en).split(';')]: # relevant only if commenting out the "(" continue above
            if en in e2c:
                del e2c[en] ; dups.add(en)
            elif not en in dups: e2c[en] = zh
    return e2c

def main():
    if sys.stdin.isatty() or len(sys.argv) < 2:
        sys.stderr.write(f"Syntax: {sys.argv[0]} cedpane.txt < input-sentences.txt")
        sys.exit(1)
    e2c = read_CedPane(sys.argv[1])
    txt = sys.stdin.read()
    trans = T(source='en', target='zh-CN')
    for tag in re.findall(r"(?:<[^>]*>\s*)+",txt,flags=re.DOTALL): e2c[tag] = tag # keep (runs of) tags, TODO: might be better if we don't make them sentence objects
    keyList = sorted(list(e2c.keys()),key=len,reverse=True)
    for i,k in enumerate(keyList): # TODO: this loop is slow: might want to get an annogen-generated annotator to do it (but there's the \b) or make an OR list like the annogen normaliser
        if k.startswith("<"): txt = txt.replace(k," {%d} " % i) # irrespective of word boundaries
        else: txt = re.sub(r"\b"+re.escape(k)+r"\b"," {%d} " % i, txt, flags=0 if re.search("[A-Z]",k) else re.IGNORECASE) # (don't match lower case if we have upper case, as it might be a name or abbreviation that in lower case will be a normal word and not this entry, but do match title case if we are lower case)
    sentences = re.findall(r"[^ .!?].*?(?:$|[.!?])(?=$|\s+)",txt,flags=re.DOTALL)
    # print("Debugger:",sentences)
    for zh in trans.translate_batch(sentences):
        for i,k in enumerate(keyList): zh = re.sub((r" *[{]%d[}] *" % i),e2c[k],zh)
        print (zh.replace("?","？").replace(",","，").replace(";","；").replace(":","：").replace(".","。").replace("▁","").replace("(","（").replace(")","）"))
        sys.stdout.flush() # in case watching

if __name__=="__main__": main()
