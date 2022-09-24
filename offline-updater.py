#!/usr/bin/env python2

# offline-updater v1.02, Silas S. Brown 2013, public domain
# - chooses packaged files to copy to an offline system

existing_files = "existing-files" # if this file exists,
# it's expected to be the output of
# find /[belorsuv]* -type f -print0 | xargs -0 ls --full-time
# on the target machine (or a fresh non-network install)

get_debs = 0
# set this to 1 to re-download the deb files for installed
# packages, instead of packing the existing system files.
# You can install on the other system with: dpkg -i *.deb
# sometimes you might need: dpkg --force-depends -i *.deb
# (the latter is usually if some dependency version number
# is slightly different but contents is identical; see the
# TODO comment below about different versions; it might
# also be because include_essential below was left at 0,
# see comments there as well)
# If the machine will later be connected to the Internet without you, you might wish to do:
# (echo apt-get update; echo apt-get -yf install) | sudo at -M midnight

use_bzip2 = 0
# - set this to 1 if you are sure the target system has
# the bzip2 command (usually there by default in modern
# distributions, but not necessarily in old ones).  Will
# automatically be set if /bin/bzip2 is in existing_files
# (as long as there's a /bin/bzip2 on THIS machine also).

use_xz = 0
# - set this to 1 if you are sure the target system has
# the xz command; will automatically be set if /usr/bin/xz
# is in existing_files (as long as there's a /usr/bin/xz
# on THIS machine also).

xz_memlimit = "150MiB" # adjust if you have more/less RAM
# (requirements of the target machine will be lower)

include_recommends = 1
# - set this to 0 to omit Recommends: packages and include
# only Depends: (this was the default behaviour of apt-get
# when installing packages in some older distributions)

include_essential = 0
# - set this to 1 to include packages marked "essential"
# by apt, which are highly likely to be already on the
# system (although not necessarily the latest version).
# Might want to set this to 1 if using get_debs to ease
# dependency problems, although it does increase the
# amount of data to be transported, and the system can
# often do without these upgrades if all you're doing is
# installing an application and its dependencies on a
# "stable" distribution (your mileage may vary however).
# Might want to set it to 1 if you're on a "rolling"
# distribution (but it's probably not a good idea to
# run one of those offline).

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

import commands, os, re, sys

def installed_list(packagename):
    f = "/var/lib/dpkg/info/"+packagename+".list"
    if os.path.isfile(f): return f
    # might still have it if :i386 or whatever is on the end
    for f in infoList:
        if f.startswith(packagename+':'):
            return "/var/lib/dpkg/info/"+f
infoList = os.listdir("/var/lib/dpkg/info")

def is_essential(packagename): return commands.getoutput('apt-cache show "%s"' % packagename).find("\nEssential: yes\n") > -1

def get_depends(packagename):
    "Yields all immediate dependencies of packagename.  Also yields recommended dependencies if include_recommends is set."
    meta_mode = 0
    for line in commands.getoutput('apt-cache depends "'+packagename+'"').split("\n"):
        if ':' in line:
            field,value = line.split(':',1)
            field,value = field.strip(), value.strip()
            if field.endswith("Depends") or (include_recommends and field.endswith("Recommends")):
                if value.startswith('<'): meta_mode = 1
                else:
                    meta_mode = 0
                    yield value
        elif meta_mode and line.strip() and not '<' in line:
            yield line.strip() # one of the options

def recursive_depends(packagenames):
    "As get_depends, but takes a list of packages, recurses, removes duplicates and limits itself to packages that are actually installed on the system (and not essential if include_essential is false).  Includes the packages listed in packagenames itself in the generated list."
    seen = {} # don't use set() as won't run on old Python
    def rd_inner(pn):
        if pn in seen: return
        seen[pn]=1
        if not installed_list(pn): return
        if (not include_essential) and is_essential(pn): return
        yield pn
        for p in get_depends(pn):
            for pp in rd_inner(p): yield pp
    for packagename in packagenames:
        for p in rd_inner(packagename): yield p

def files(packagename):
    "Assuming packagename is installed, yields the files and symlinks from packagename that are present on the machine"
    for l in open(installed_list(packagename)):
        l = l.strip()
        if os.path.isfile(l) or os.path.islink(l): yield l

def normalise_ls(ls): return re.sub(r'\.00* ',' ',re.sub('  *',' ',ls.strip()))

wrong = len(sys.argv) < 2
if not wrong:
    packages = sys.argv[1:]
    for p in packages:
        if not installed_list(p):
            sys.stderr.write("Package '%s' is not installed\n" % p)
            wrong = 1
if wrong:
    sys.stderr.write("Syntax: %s package-names\n" % sys.argv[0])
    sys.exit(1)

try: existing_files = open(existing_files)
except: existing_files,existing_files_asStr = {},""
if existing_files:
    r = {}
    for f in existing_files: r[normalise_ls(f)] = 1
    existing_files = r
    existing_files_asStr = "/".join(r.keys())
    def chk(f):
        if "/bin/"+f in existing_files_asStr:
            if os.path.exists(commands.getoutput("which "+f+" 2>/dev/null")): return 1
            else: sys.stderr.write("Note: target machine's existing_files has "+f+" but we can't take advantage of that because there is no local "+f+"\n")
        return 0
    use_bzip2 = chk("bzip2") ; use_xz = chk("xz")

def isNew(fname):
    if fname not in existing_files_asStr: return 1
    return not normalise_ls(commands.getoutput('ls --full-time "%s"' % fname)) in existing_files

def package_is_new(packagename):
    for f in files(packagename):
        if isNew(f): return 1
    # TODO: what if a package has 2 or more different versions with identical contents but treated as different for dependency resolution?
    # (currently we assume it's not really new if all the files it installed were there already with the same size/times/permissions;
    # this should work in practice but might confuse dpkg and require --force-depends,
    # and apt-get might need to be run with -f later.)

if len(packages)==1: output=packages[0]+".tar"
else: output="files.tar"

try: os.remove(output)
except: pass
# (must start with not exist, because xargs uses multiple
# invocations of 'tar -r' to append to it)

if get_debs:
    print "get_debs is True: computing which .deb files to fetch"
    deb_sources = commands.getoutput("grep '^ *deb  *http' < /etc/apt/sources.list").split("\n")
    tryUrls = [] ; pkgs = []
    for p in recursive_depends(packages):
        if package_is_new(p):
            fname = commands.getoutput('apt-cache show "'+p+'"|grep ^Filename:|head -1').replace("Filename: ","")
            assert fname.startswith("pool/")
            section=fname[5:fname.index('/',5)]
            pkgs.append(fname[fname.rindex('/')+1:])
            for s in deb_sources:
                if (s+" ").find(" "+section+" ")>-1:
                    tryUrls.append('"'+s.split()[1]+'/'+fname+'"')
    print "Running wget (don't worry about 404s)"
    # (TODO: should really do better parsing of apt files
    # instead of brute-force trying all possible URLs, but
    # careful of backward compatibility with old distros.)
    os.system('wget -c '+' '.join(tryUrls))
    errs = 0
    for p in pkgs:
        if not os.path.isfile(p):
            print "ERROR: Failed to get "+p
            errs = 1
    if not errs:
        print "All files downloaded OK (ignore any 404 errors above)"
        os.system("du -hc "+" ".join(pkgs))
else:
    print "get_debs is False: packaging existing files"
    tar = os.popen("xargs -0 tar -rvf "+output,"w")
    filesSeen = {}
    for p in recursive_depends(packages):
        for f in files(p):
            if f in filesSeen: continue
            filesSeen[f] = 1
            if not isNew(f): continue
            # TODO: option to omit /usr/share/doc files to save space?
            tar.write(f+chr(0))
        # TODO: option to update /var/lib/dpkg/status and add /var/lib/dpkg/info/packagename... files ?
        # (status update won't be a simple .tgz though; might be better to take the .debs if dpkg still working)
    tar.close()
    if use_xz: os.system('xz -9 "--memlimit=%s" "%s" ; du -h "%s.xz"' % (xz_memlimit,output,output))
    elif use_bzip2: os.system('bzip2 -9 "%s" ; du -h "%s.bz2"' % (output,output))
    else: os.system('gzip -9 "%s" ; du -h "%s.gz"' % (output,output))
    # TODO bz2 sometimes smaller than xz for text, can we mix?
