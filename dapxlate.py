#!/usr/bin/env python3

"""DAPXlate - Dictionary-Assisted Pretrained Translate
  v0.1 (c) Silas S. Brown 2024, License: Apache 2

  - Uses a pretrained translator model
    (currently 2020's OPUS-MT via argostranslate)
    but adds specialist name translation from
    (latest) CedPane w/out needing to retrain the
    model.  Does this by having the model handle
    placeholders for words we're sure we know how
    to translate ourselves from the dictionary.

    (This model can't cope with pre-translated
     fragments in the target language, so it's
     necessary to use the placeholders.)

  PROBLEMS:

    - Slow.  (15 minutes for a ~5k word document
              on quad-core ARM w/out CUDA)

    - Resulting translation still needs extensive
      proofreading and editing :-(
      (can emit bogus escape codes etc also)

"""

def install():
    os.system("""set -e
    git clone https://github.com/argosopentech/argos-translate
    cd argos-translate
    git checkout f8cadf001224d751a30125193a084670d8026ed1 # the version I tested
    pip install -e .""") # because pip install argos-translate had an error.  Note that this command links the install to the current "argos-translate" directory, which should then not be removed.
    import argostranslate.package
    argostranslate.package.update_package_index()
    argostranslate.package.install_from_path([x for x in argostranslate.package.get_available_packages() if x.from_code=="en" and x.to_code=="zh"][0].download())

def uninstall_argos_deps():
    os.system("pip uninstall sentencepiece mpmath typing-extensions tqdm sympy regex numpy networkx joblib fsspec filelock torch sacremoses ctranslate2 stanza") # TODO: more on x86
    print ("Might also want: rm -rf argos-translate")

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

def test():
    if sys.stdin.isatty() or len(sys.argv) < 2:
        sys.stderr.write(f"Syntax: {sys.argv[0]} cedpane.txt < input-sentences.txt")
        sys.exit(1)
    e2c = read_CedPane(sys.argv[1])
    txt = sys.stdin.read()
    for tag in re.findall(r"(?:<[^>]*>\s*)+",txt,flags=re.DOTALL): e2c[tag] = tag # keep (runs of) tags, TODO: might be better if we don't make them sentence objects
    keyList = sorted(list(e2c.keys()),key=len,reverse=True)
    for i,k in enumerate(keyList): # TODO: this loop is slow: might want to get an annogen-generated annotator to do it (but there's the \b) or make an OR list like the annogen normaliser.  But it's nowhere near the worst bottleneck (argostranslate w/out CUDA)
        if k.startswith("<"): txt = txt.replace(k," {%d} " % i) # irrespective of word boundaries.  Spacing important.  "I went to {1}Paris{2} last summer." upsets the model, as does doing it via Tags, as does using letters not numbers in the {}s
        else: txt = re.sub(r"\b"+re.escape(k)+r"\b"," {%d} " % i, txt, flags=0 if re.search("[A-Z]",k) else re.IGNORECASE) # (don't match lower case if we have upper case, as it might be a name or abbreviation that in lower case will be a normal word and not this entry, but do match title case if we are lower case)
    import argostranslate.translate
    # TODO: might now want FAHClient --send-pause because xlator averages 2.5 cores and can read 3.5 (on a 4-core CPU)
    for sentence in re.findall(r"[^ .!?].*?(?:$|[.!?])(?=$|\s+)",txt,flags=re.DOTALL):
        # print (sentence) # if want to show which phrases are NOT given to the model
        zh = argostranslate.translate.translate(sentence,'en','zh')
        for i,k in enumerate(keyList): zh = re.sub((r" *[{]%d[}] *" % i),e2c[k],zh)
        print (zh.replace("?","？").replace(",","，").replace(";","；").replace(":","：").replace(".","。").replace("▁","").replace("(","（").replace(")","）"))
        # print("") # if printing English above
        sys.stdout.flush() # in case watching

if __name__=="__main__": test()
