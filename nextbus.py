"""
nextbuses.mobi fetch next 2 buses for specific stop
Silas S. Brown 2025 - public domain - no warranty

You need to set busStopCode below.

You can then use this either on the command line or as an Alexa skill.

To deploy to your Alexa devices: Go to developer.amazon.com to add
the developer role to your Amazon account, and under "Alexa Skills
Kit" Console use "Create Skill", name it, set model type to "Custom",
hosting type to "Alexa-hosted (Python)", template start from scratch
then under "Interaction Model" choose "JSON Editor" and paste this:

{"interactionModel": { "languageModel": {
     "invocationName": "next bus",
     "intents": [
       {"name": "InputIntent","slots": [],"samples": ["next bus"]},
       {"name": "AMAZON.HelpIntent",  "samples": []},
       {"name": "AMAZON.CancelIntent","samples": []},
       {"name": "AMAZON.StopIntent",  "samples": []}], "types":[]}}}

Save and Build, then under "Code" replace all the content with this
file, Save and Deploy, then under Test enable testing and try saying
"open Next Bus".

If there's an error go back to Code and check under CloudWatch Logs.
"""

busStopCode = "TODO: SET THIS"
import requests, re, time
def _untracked(m):
    # assume clock time means untracked
    mins = int((time.mktime(time.localtime()[:3]+tuple(int(x) for x in m.group().split(':'))+time.localtime()[5:])-time.time())/60)
    return "untracked "+str(mins)+" minute"+("" if mins==1 else "s")
def next_buses():
    return " and ".join(re.sub("^[0-9]+:[0-9][0-9]",_untracked,re.sub(".* DUE","due",re.sub(".* (in|at) ","",t.replace("min","minute")))) for t in re.findall('(?<=<p class="Stops">)[^<]*(?=</p>)',requests.get("https://nextbuses.mobi/WebView/BusStopSearch/BusStopSearchResults/"+busStopCode.lower()).content.decode('utf-8'))[:2])

def lambda_handler(event, context):
    if event['request']['type'] not in ['AMAZON.StopIntent','AMAZON.CancelIntent']:
        return {'version': '1.0','response':{'outputSpeech': {
            'type':'PlainText','text':next_buses(),
            'shouldEndSession':True}}}

if __name__ == "__main__": print(next_buses())
