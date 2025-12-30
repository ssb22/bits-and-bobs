#!/usr/bin/env python3
"""Backport Telegram Desktop's "Export chat history" JSON
to the format used by a much older version of Telegram Desktop.

(e.g. Telegram Desktop 1.8.15 for Mac, the last version to work
in Mac OS X 10.7 on an old 2011 Mac Mini: this version stopped
being able to communicate with Telegram's servers in November 2025.)

Use for when you want to export Saved Messages in the same format
as before because you have scripts that handle the old format.

Silas S. Brown 2025 - public domain - no warranty."""

import json
for msg in json.load(open("result.json"))["messages"]:
    if not msg['text'] or not 'from' in msg: continue
    mDate,mTime = msg['date'].split('T')
    Y,M,D = mDate.split('-') ; h,m,s = mTime.split(':')
    print(f"{msg['from']}, [{D}.{M}.{Y[-2:]} {h}:{m}]\n{''.join(i["text"] if type(i)==dict else i for i in msg['text']) if type(msg['text'])==list else msg['text']}\n")
