#!/usr/bin/env python3

"""DAPXlate - Dictionary-Assisted Pretrained Translate
  (or Domain-Adaptation with Placeholders translation)
  v0.3 (c) Silas S. Brown 2024, License: Apache 2

  - Uses a pretrained translator model online
    but adds specialist phrase translations.
    Extracts first draft of these from CedPane
    then lets you edit before re-running with the
    model.  Does this by having the model handle
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

    - Extracted list from CedPane very much needs
      editing before the run

    - Resulting translation still needs editing
"""

from deep_translator import GoogleTranslator as T
# (you could use another if you have an API key)
import re, sys, os, time

def read_CedPane(cedpane_file):
    "Extract potential specialist translations and names from CedPane, for editing"
    dups = set() # avoid translating if we're not sure (TODO: sometimes it's OK to pick one)
    e2c = {}
    for en,zh in [l.split("\t")[:2] for l in open(cedpane_file).read().split("\n")[1:-1]]:
        if "translation" in en or "incorrect" in en or re.search(r"\btypo\b",en): continue # alternate translation, old translation, typo, etc
        en = re.sub(" ([^)]*name[^)]*)","",en) # "X (surname)" is ok if X is capitals only
        if "(" in en: continue # we don't want entries like "notice (on paper)" where the parens indicate it's a specific meaning
        if re.search("; [^A-Z]",en): continue # "here; in this region" probably shouldn't pull out "here", but ";" + abbreviation is probably OK, as is "Name; Name"
        for en in [een.strip() for een in re.sub("[(][^)]*[)]","",en).split(';')]: # relevant only if commenting out the "(" continue above
            if en in e2c:
                del e2c[en] ; dups.add(en)
            elif not en in dups: e2c[en] = zh
    return e2c

def main():
    if sys.stdin.isatty() and len(sys.argv) < 2:
        sys.stderr.write(f"Syntax: {sys.argv[0]} cedpane.txt (makes Chinese.tsv)\nor {sys.argv[0]} < input-sentences.txt\n")
        sys.exit(1)
    if os.path.exists("Chinese.tsv"): e2c=dict(i.strip().split('\t') for i in open("Chinese.tsv").read().split('\n') if '\t' in i.strip())
    else: e2c = read_CedPane(sys.argv[1])
    txt = sys.stdin.read()
    trans = T(source='en', target='zh-CN')
    for tag in re.findall(r"(?:<[^>]*>\s*)+",txt,flags=re.DOTALL): e2c[tag] = tag # keep (runs of) tags, TODO: might be better if we don't make them sentence objects
    keyList = sorted(list(e2c.keys()),key=len,reverse=True)
    e2c_real = {}
    t = time.time()
    for i,k in enumerate(keyList): # TODO: this loop is slow: might want to get an annogen-generated annotator to do it (but there's the \b) or make an OR list like the annogen normaliser
        if time.time() > t+2:
            sys.stderr.write(f"\r{i}/{len(keyList)} (found {len(e2c_real)})... ")
            sys.stderr.flush() ; t = time.time()
        if k.startswith("<"): txt = txt.replace(k," {%d} " % i) # irrespective of word boundaries
        else:
            txt = re.sub(r"\b"+re.escape(k)+r"\b"," {%d} " % i, txt, flags=0 if re.search("[A-Z]",k) else re.IGNORECASE) # (don't match lower case if we have upper case, as it might be a name or abbreviation that in lower case will be a normal word and not this entry (TODO there can be false positives at start of sentences though), but do match title case if we are lower case)
            if (" {%d} " % i) in txt:
                e2c_real[k]=e2c[k]
    if not os.path.exists("Chinese.tsv"): 
        open("Chinese.tsv","w").write("".join(f"{e}\t{c}\n" for e,c in sorted(e2c_real.items())))
        print ("Wrote Chinese.tsv: edit it before rerun")
        return
    sentences = re.findall(r"[^ .!?].*?(?:$|[.!?])(?=$|\s+)",txt,flags=re.DOTALL) # TODO: at one point didn't include a <p> (prob repr'd as {..}) at start of sentence, regex seems ok, did model drop it?
    # print("Debugger:",sentences)
    for zh in trans.translate_batch(sentences):
        for i,k in enumerate(keyList): zh = re.sub((r" *[{]%d[}] *" % i),e2c[k],zh)
        print (zh.replace("?","？").replace(",","，").replace(";","；").replace(":","：").replace(".","。").replace("▁","").replace("(","（").replace(")","）"))
        sys.stdout.flush() # in case watching

if __name__=="__main__": main()
