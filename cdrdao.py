#!/usr/bin/env python
# (should work in either Python 2 or Python 3)

# cdrdao track padder, 2012, 2020 Silas S. Brown. Public domain.
# Version 1.4

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

cd_frames = 359845 # 79min 57sec 70/75 frames, typical for 700M "80min" CDs

absolute_minimum_silent_frames = 2 * 75

import os,sys,os.path
if len(sys.argv) < 2:
    print ("Syntax: cdrdao.py sound-files")
    sys.exit(1)

filelist = []
frames_this_cd = 0 ; cd_starts = [] # 1st try: pack them as they come
total_frames = 0
for f in sys.argv[1:]:
    f2 = "rawfile%d" % len(filelist)
    print ("Converting "+f)
    ret = os.system("sox \"%s\" -t raw -B -b 16 -e signed-integer -c 2 -r 44100 %s" % (f,f2))
    assert not ret, "sox error"
    frames = int((os.stat(f2).st_size+2351)/2352) # round up
    if frames_this_cd: frames_this_cd += absolute_minimum_silent_frames
    if not cd_starts or frames_this_cd + frames > cd_frames:
        cd_starts.append(len(filelist))
        frames_this_cd = 0
    frames_this_cd += frames
    total_frames += frames
    f = os.path.basename(f)
    if '.' in f: f=f[:f.rindex('.')]
    filelist.append((frames,f2,f))

print ("Fitting onto %d CDs" % len(cd_starts))

average_frames = total_frames/len(cd_starts)
i = len(cd_starts)-1 ; topF = len(filelist)
def totframes(start,end): return sum([f for f,f2,_ in filelist[start:end]])
while i:
    # if CD 'i' has above average gaps (below average total
    # frames), try to get it as close as possible to the
    # average by pulling tracks over from CD i-1
    while totframes(cd_starts[i],topF) < average_frames and abs(average_frames-totframes(cd_starts[i],topF)) > abs(average_frames-totframes(cd_starts[i]-1,topF)) and totframes(cd_starts[i]-1,topF) < cd_frames-absolute_minimum_silent_frames*(topF-cd_starts[i]-2): # (-2 as 1st track doesn't need lead-in)
        cd_starts[i] -= 1
        assert cd_starts[i], "non-1st CD reached 0 ?!?"
        j = i
        while j and cd_starts[j-1] >= cd_starts[j]:
            j -= 1
            assert cd_starts[j],"second CD reached 0 ?!?"
            cd_starts[j] -= 1
    topF = cd_starts[i]
    i -= 1

for i in range(len(cd_starts)):
    fn = "cd%d.toc" % (i+1,)
    o=open(fn,"w")
    if i==len(cd_starts)-1: topF = len(filelist)
    else: topF = cd_starts[i+1]
    o.write("CD_DA\nCD_TEXT {\n  LANGUAGE_MAP {\n    0 : EN\n  }\n  LANGUAGE 0 {\n    TITLE \"CD %d (%s to %s)\"\n  }\n}\n\n" % (i,filelist[cd_starts[i]][2],filelist[topF-1][2]))
    pregap = 0
    for track in range(cd_starts[i],topF):
        if pregap: pgstr = "PREGAP %d:%d:%d\n" % (pregap/(60*75),(pregap%(60*75))/75,(pregap%75))
        else: pgstr = ""
        o.write("TRACK AUDIO\nCD_TEXT {\n  LANGUAGE 0 {\n    TITLE \"%s\"\n  }\n}\n%sFILE \"%s\" 0\n\n" % (filelist[track][2],pgstr,filelist[track][1]))
        if not pregap and topF>cd_starts[i]+1: pregap = (cd_frames-totframes(track,topF))/(topF-cd_starts[i]-1)
    o.close()
    if cd_starts[i]: trackinfo="-%d" % cd_starts[i]
    else: trackinfo=""
    print ("You can now do: cdrdao write "+fn+(" # (%d to %d, track=number%s)" % (cd_starts[i]+1,topF,trackinfo)))
print ("When finished, you can do: rm *.toc rawfile*")
