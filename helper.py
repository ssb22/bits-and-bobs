"""Python Helper for Alexa.  Allows a beginner to write Python code
calling print(), input(), random and time.  Repeats their values as
necessary to restore state for further interactions.
Version 1.1 (c) Silas S. Brown 2025.  No warranty.

To deploy to your Alexa devices: Go to developer.amazon.com to add
the developer role to your Amazon account, and under "Alexa Skills
Kit" use "Create Skill", name it, set model type to "Custom",
hosting type to "Alexa-hosted (Python)", template start from scratch
then under "Interaction Model" choose "JSON Editor" and paste this:

{"interactionModel": { "languageModel": {
     "invocationName": "python helper",
     "intents": [
       {"name": "InputIntent","slots": [{"name": "UserInput","type": "AMAZON.SearchQuery"}],"samples": ["answer {UserInput}"]},
       {"name": "AMAZON.HelpIntent",  "samples": []},
       {"name": "AMAZON.CancelIntent","samples": []},
       {"name": "AMAZON.StopIntent",  "samples": []}], "types":[]},
     "prompts":[{"id":"1","variations":[{"type":"PlainText","value":"Waiting for input"}]}],
     "dialog": {"intents": [{"name": "InputIntent","confirmationRequired": false,"prompts": {},"slots":[{"name": "UserInput","type":"AMAZON.SearchQuery","confirmationRequired": false,"elicitationRequired": true,"prompts":{"elicitation":"1"}}]}],"delegationStrategy": "SKILL_RESPONSE"}}}

Save and Build, then under "Code" replace all the content with this
file, Save and Deploy, then under Test enable testing and try saying
"open Python Helper".
You should be able to answer your program's questions just by speaking.
If that doesn't work, try saying the word "answer" before your answer.

If there's an error go back to Code and check under CloudWatch Logs.
"""

import time,random,inspect,sys
class FunctionWrapper:
  def __init__(self): self.logs = {}
  def wrapF(self,func,call_real_again = False):
    k = f"{func.__module__}.{func.__name__}"
    def iterator(args,kw):
        self.logs.setdefault(k,[])
        for i in self.logs[k]:
            if call_real_again: func(*args,**kw)
            args,kw=(yield i)
        while True:
            i = func(*args,**kw)
            self.logs[k].append(i)
            args,kw=(yield i)
    it = []
    def newFunc(*args,**kw):
        if it: return it[0].send((args,kw))
        it.append(iterator(args,kw))
        return it[0].send(None) # 1st value
    newFunc.oldFunc=func
    return newFunc
  def wrapM(self,module,again=False):
    for n,m in inspect.getmembers(module,lambda x:any(f(x) for f in [inspect.isfunction,inspect.ismethod,inspect.isbuiltin])):
      setattr(module,n,self.wrapF(m,again))
  def unwrapM(self,module):
    for n,m in inspect.getmembers(module,inspect.isfunction): setattr(module,n,m.oldFunc)
fw = FunctionWrapper()
def print(*P): fw.outBuf.append(' '.join(f'{a}'for a in P))
def input(prompt=None):
  if prompt is not None: print(prompt)
  fw.inputWait = True ; sys.exit()
def wrapPrintInput():
  try:    __builtins__.print   =fw.wrapF(print)
  except: __builtins__['print']=fw.wrapF(print)
  try:    __builtins__.input   =fw.wrapF(input)
  except: __builtins__['input']=fw.wrapF(input)

def lambda_handler(event, context):
  fw.outBuf,fw.inputWait,fw.logs = [],False,{}
  if event['session'].get('new',False): fw.outBuf=["Python program starting."]
  else: fw.logs=event['session']['attributes']
  shouldRun = True
  if event['request']['type']=='IntentRequest':
    iName = event['request']['intent']['name']
    if iName == 'InputIntent': fw.logs.setdefault(__name__+'.input',[]).append(event['request']['intent']['slots'].get('UserInput', {}).get('value',''))
    elif iName == 'AMAZON.HelpIntent': fw.outBuf.append("Speak the input to your program.")
    elif iName == 'AMAZON.StopIntent' or iName == 'AMAZON.CancelIntent': shouldRun = False
  if shouldRun:
    fw.wrapM(time),fw.wrapM(random,True),wrapPrintInput()
    try: exec(user_code,{})
    except SystemExit: pass
    except Exception as e: fw.outBuf += [f"Unhandled {type(e)} {e}"]
    fw.unwrapM(time),fw.unwrapM(random)
  if fw.inputWait:
    if not fw.outBuf: fw.outBuf=["Waiting"]
  else: fw.outBuf += ["Program terminated"]
  r={'version': '1.0','response':{'outputSpeech': {
       'type':'PlainText','text':'\n'.join(fw.outBuf)},
      "reprompt":{"outputSpeech":{"type":"PlainText",
        "text":'\n'.join([i for i in fw.outBuf if i.strip()][-1:])}},
      'shouldEndSession': not fw.inputWait}}
  if fw.inputWait: r['response']['directives'],r['sessionAttributes']=[{"type":"Dialog.ElicitSlot","slotToElicit":"UserInput"}],fw.logs
  return r

user_code = r'''

# Delete this example and paste the child's code here:
import random, sys
answer = random.randint(1,10)
while True:
  i = int(input("Guess my number: "))
  if i < answer: print("That's too low")
  elif i > answer: print("That's too high")
  else: print("Correct"), sys.exit()
# End of example.  Please do NOT delete the apostrophes below.

'''
