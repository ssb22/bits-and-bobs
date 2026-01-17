"""
Cambridge next bin collection
Silas S. Brown 2026 - public domain - no warranty

You need to set your UPRN (unique property reference number)
You can then use this either on the command line or as an Alexa skill.

To deploy to your Alexa devices: Go to developer.amazon.com to add
the developer role to your Amazon account, and under "Alexa Skills
Kit" Console use "Create Skill", name it, set model type to "Custom",
hosting type to "Alexa-hosted (Python)", region EU (avoids possible time
zone issues), template start from scratch, then under "Interaction Model"
choose "JSON Editor" and paste this:

{"interactionModel": { "languageModel": {
     "invocationName": "next bin collection",
     "intents": [
       {"name":"InputIntent","slots":[],"samples":["next bin collection"]},
       {"name": "AMAZON.HelpIntent",  "samples": []},
       {"name": "AMAZON.CancelIntent","samples": []},
       {"name": "AMAZON.StopIntent",  "samples": []}], "types":[]}}}

Save and Build, then under "Code" replace all the content with this
file, Save and Deploy, then under Test enable testing and try saying
"Next bin collection".

If there's an error go back to Code and check under CloudWatch Logs.
"""

UPRN = "TODO: SET THIS" # (do not check into any public repository: it identifies your exact home address)
import requests, re, time, json

def next_bins():
    firstDate,colours = None,[]
    for colour,_,date in [label.partition(" bin collection on ") for label in re.findall(r'(?<=aria-label=")[^"]+',json.loads(requests.get(f"https://www.greatercambridgewaste.org/bin-calendar/collections?uprn={UPRN}&numberOfCollections=12",headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (actually nextbin.py)"}).content.decode('utf-8'))['refuseCollectionInfo'])]: # fake User-Agent required if fetching from an AWS IP, but please include an "actually" in case anyone needs to check logs
         if not colour or not date: continue # in case any other aria-label
        if firstDate and not date==firstDate:
            if firstDate==time.strftime("%A %d %B %Y"): spokenDate = " today"
            elif firstDate==time.strftime("%A %d %B %Y",time.localtime(time.time()+24*3600)): spokenDate = " tomorrow"
            elif firstDate==time.strftime("%A %d %B %Y",time.localtime(time.time()-24*3600)): spokenDate = " yesterday" # this can happen (if a collection is delayed?)
            elif 0 < time.mktime(time.strptime(firstDate,"%A %d %B %Y"))-time.time() < 6*24*3600: spokenDate = f" on {firstDate.split()[0]}"
            elif -6*24*3600 < time.mktime(time.strptime(firstDate,"%A %d %B %Y"))-time.time() < 0: spokenDate = f" last {firstDate.split()[0]}"
            else: spokenDate = f" on {' '.join(firstDate.split()[:3])}"
            return " and ".join(colours) + spokenDate
        firstDate = date ; colours.append(colour)
    return "Council website error or format change"

def lambda_handler(event, context):
    if event['request']['type'] not in ['AMAZON.StopIntent','AMAZON.CancelIntent']:
        return {'version': '1.0','response':{'outputSpeech': {
            'type':'PlainText','text':next_bins(),
            'shouldEndSession':True}}}

if __name__ == "__main__": print(next_bins())
