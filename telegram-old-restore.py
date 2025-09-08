"""
Restore Telegram conversation from OLD export format
(i.e. from telegram-backport.py output)

Silas S. Brown 2025 - public domain - no warranty

Share the resulting "WhatsApp" zip with Telegram to import.
Might not be able to restore to Saved Messages.
Can restore to a group chat with self, but:
* "edit message" may not be available on the resulting messages (can just copy / add new and delete, changing timestamp)
* old Telegram 1.8.15 on Mac OS 10.7 on old machine whose OS cannot be upgraded won't see the new group chat (messages need forwarding individually to Saved Messages to be available on that)
"""

import re, sys
def msgs():
    r = [] ; canMatch = True
    for l in sys.stdin:
        l=l.rstrip()
        if canMatch: m=re.match(r"(.+), \[([0-3][0-9])\.([01][0-9])\.([0-9]{2}) ([0-2][0-9]):([0-5][0-9])\]$",l)
        else: m = None
        canMatch = not l
        if m:
            if r: yield ''.join(r[:1]+[i+'\n' for i in r[1:]])
            mFrom,mD,mM,mY,mh,mm = m.groups()
            # TODO: need to translate that time to the *current* time zone.  E.g. if we're now in summer time and that date is winter time, need to + 1 hour, otherwise it will go in as an hour before it really was.  So the season at which the zip is imported (assumed same as when generated?) affects which time we should use.
            r=[f"[20{mY}/{mM}/{mD}, {mh}:{mm}:00] {mFrom}: "]
        elif r: r.append(l)
    if r: yield ''.join(r[:1]+[i+'\n' for i in r[1:]])

from zipfile import ZipFile, ZIP_DEFLATED
z = ZipFile("WhatsApp Chat - Messages.zip","w",ZIP_DEFLATED)
z.writestr('_chat.txt',''.join(msgs()))
z.close()
